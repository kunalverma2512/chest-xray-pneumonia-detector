"""
backend/app/ml/training.py

Training entry point that wraps the existing scripts/train_model.py logic.

All hyper-parameters and model architecture are **unchanged** from the original
ChestXRayTrainer class.  This module simply makes the training callable as a
library function (importable) so that:
  - scripts/run_training.py can invoke it as a CLI script.
  - future orchestration (Airflow, Prefect, etc.) can call it programmatically.

Key design decisions:
  - Paths are resolved from ``settings`` rather than hard-coded relative paths.
  - The class retains the same public API as the original.
  - No TF/Keras logic has been altered.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional, Tuple

import matplotlib
matplotlib.use("Agg")          # Non-interactive backend – safe for headless runs
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

from app.core.config import settings

logger = logging.getLogger(__name__)

# Suppress TF C++ logs
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import tensorflow as tf  # noqa: E402
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    ReduceLROnPlateau,
)
from tensorflow.keras.optimizers import Adam


class ChestXRayTrainer:
    """
    MobileNetV2-based chest X-ray classifier trainer.

    Identical architecture and hyper-parameters to the original
    scripts/train_model.py.  Paths are now sourced from ``settings``.
    """

    def __init__(
        self,
        img_size: int = settings.train_img_size,
        batch_size: int = settings.train_batch_size,
    ) -> None:
        self.img_size = img_size
        self.batch_size = batch_size
        self.model: Optional[tf.keras.Model] = None
        self.history = None

        models_dir = Path(settings.models_dir)
        models_dir.mkdir(parents=True, exist_ok=True)

        logger.info(
            "ChestXRayTrainer initialised | img=%dx%d | batch=%d",
            img_size,
            img_size,
            batch_size,
        )

    # ------------------------------------------------------------------
    # Data generators
    # ------------------------------------------------------------------

    def create_data_generators(self):
        """
        Create Keras ImageDataGenerators for train / val / test splits.

        Returns:
            Tuple of (train_generator, val_generator, test_generator).
            Returns (None, None, None) on failure.
        """
        data_path = Path(settings.processed_data_dir)
        logger.info("Looking for processed data at: %s", data_path.absolute())

        if not data_path.exists():
            logger.error("Processed data not found at %s", data_path)
            return None, None, None

        for split in ("train", "val", "test"):
            if not (data_path / split).exists():
                logger.error("Missing data split folder: %s", data_path / split)
                return None, None, None

        train_datagen = ImageDataGenerator(
            rescale=1.0 / 255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2],
            fill_mode="nearest",
        )
        # Validation / test: normalisation only
        val_datagen = ImageDataGenerator(rescale=1.0 / 255)

        common_kwargs = dict(
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode="binary",
        )

        train_generator = train_datagen.flow_from_directory(
            data_path / "train", shuffle=True, seed=42, **common_kwargs
        )
        val_generator = val_datagen.flow_from_directory(
            data_path / "val", shuffle=False, **common_kwargs
        )
        test_generator = val_datagen.flow_from_directory(
            data_path / "test", shuffle=False, **common_kwargs
        )

        logger.info(
            "Data generators created | train=%d val=%d test=%d | classes=%s",
            train_generator.samples,
            val_generator.samples,
            test_generator.samples,
            train_generator.class_indices,
        )
        return train_generator, val_generator, test_generator

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    def build_model(self) -> tf.keras.Model:
        """
        Construct MobileNetV2 with a custom classification head.

        Architecture (identical to original):
          MobileNetV2 (frozen, imagenet weights)
          → GlobalAveragePooling2D
          → Dropout(0.3)
          → Dense(128, relu)
          → Dropout(0.2)
          → Dense(1, sigmoid)
        """
        base_model = MobileNetV2(
            weights="imagenet",
            include_top=False,
            input_shape=(self.img_size, self.img_size, 3),
        )
        base_model.trainable = False  # Freeze during initial training phase

        self.model = Sequential(
            [
                base_model,
                GlobalAveragePooling2D(),
                Dropout(0.3),
                Dense(128, activation="relu", name="dense_1"),
                Dropout(0.2),
                Dense(1, activation="sigmoid", name="predictions"),
            ]
        )

        self.model.compile(
            optimizer=Adam(learning_rate=settings.train_learning_rate),
            loss="binary_crossentropy",
            metrics=["accuracy", "precision", "recall"],
        )

        logger.info(
            "Model built | params=%d",
            self.model.count_params(),
        )
        return self.model

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def train_model(self, train_gen, val_gen, epochs: int = settings.train_epochs):
        """
        Fit the model with callbacks.

        Callbacks (identical to original):
          - ModelCheckpoint  → saves best val_accuracy weights
          - EarlyStopping    → patience=7
          - ReduceLROnPlateau→ patience=4, factor=0.5
        """
        best_model_path = str(Path(settings.models_dir) / "best_chest_xray_model.h5")

        callbacks = [
            ModelCheckpoint(
                best_model_path,
                monitor="val_accuracy",
                save_best_only=True,
                mode="max",
                verbose=1,
            ),
            EarlyStopping(
                monitor="val_accuracy",
                patience=7,
                restore_best_weights=True,
                verbose=1,
            ),
            ReduceLROnPlateau(
                monitor="val_loss",
                factor=0.5,
                patience=4,
                min_lr=1e-7,
                verbose=1,
            ),
        ]

        logger.info("Training started for %d epochs…", epochs)
        self.history = self.model.fit(
            train_gen,
            epochs=epochs,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1,
        )
        logger.info("Training completed.")
        return self.history

    # ------------------------------------------------------------------
    # Evaluation (internal test set)
    # ------------------------------------------------------------------

    def evaluate_model(self, test_gen) -> Tuple[float, str, np.ndarray]:
        """
        Evaluate the model on the internal test set and save a confusion matrix.

        Returns:
            (accuracy, classification_report_str, confusion_matrix_ndarray)
        """
        best_model_path = str(Path(settings.models_dir) / "best_chest_xray_model.h5")
        self.model.load_weights(best_model_path)

        test_gen.reset()
        predictions = self.model.predict(test_gen, verbose=1)
        predicted_classes = (predictions > 0.5).astype(int).flatten()
        true_labels = test_gen.classes

        class_names = ["Normal", "Pneumonia"]
        report = classification_report(
            true_labels, predicted_classes, target_names=class_names, digits=4
        )

        cm = confusion_matrix(true_labels, predicted_classes)
        accuracy = (cm[0, 0] + cm[1, 1]) / cm.sum()

        # Save confusion matrix plot
        self._save_confusion_matrix(cm, accuracy, class_names)

        logger.info(
            "Evaluation complete | accuracy=%.4f | normal=%.1f%% | pneumonia=%.1f%%",
            accuracy,
            (cm[0, 0] / (cm[0, 0] + cm[0, 1]) * 100) if (cm[0, 0] + cm[0, 1]) > 0 else 0,
            (cm[1, 1] / (cm[1, 1] + cm[1, 0]) * 100) if (cm[1, 1] + cm[1, 0]) > 0 else 0,
        )
        return accuracy, report, cm

    def _save_confusion_matrix(
        self, cm: np.ndarray, accuracy: float, class_names: list
    ) -> None:
        """Persist a confusion-matrix figure to the models directory."""
        out_path = Path(settings.models_dir) / "confusion_matrix.png"
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=class_names,
            yticklabels=class_names,
        )
        plt.title("Confusion Matrix – Chest X-Ray Classification", fontsize=14, fontweight="bold")
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        plt.figtext(
            0.5, 0.02, f"Overall Accuracy: {accuracy:.1%}", ha="center", fontsize=12, fontweight="bold"
        )
        plt.tight_layout()
        plt.savefig(str(out_path), dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Confusion matrix saved to %s", out_path)

    # ------------------------------------------------------------------
    # History plot
    # ------------------------------------------------------------------

    def plot_training_history(self) -> None:
        """Save a training-progress figure (accuracy / loss / precision+recall)."""
        if self.history is None:
            logger.warning("No training history available to plot.")
            return

        h = self.history.history
        out_path = Path(settings.models_dir) / "training_progress.png"

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        axes[0].plot(h["accuracy"], label="Train", linewidth=2)
        axes[0].plot(h["val_accuracy"], label="Val", linewidth=2)
        axes[0].set(title="Accuracy", xlabel="Epoch", ylabel="Accuracy")
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        axes[1].plot(h["loss"], label="Train", linewidth=2)
        axes[1].plot(h["val_loss"], label="Val", linewidth=2)
        axes[1].set(title="Loss", xlabel="Epoch", ylabel="Loss")
        axes[1].legend()
        axes[1].grid(alpha=0.3)

        axes[2].plot(h["precision"], label="Precision", linewidth=2)
        axes[2].plot(h["recall"], label="Recall", linewidth=2)
        axes[2].set(title="Precision & Recall", xlabel="Epoch", ylabel="Score")
        axes[2].legend()
        axes[2].grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(str(out_path), dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Training history plot saved to %s", out_path)


# ---------------------------------------------------------------------------
# Convenience entry-point function (called by scripts/run_training.py)
# ---------------------------------------------------------------------------

def run_training_pipeline(
    img_size: int = settings.train_img_size,
    batch_size: int = settings.train_batch_size,
    epochs: int = settings.train_epochs,
) -> bool:
    """
    Execute the full training pipeline end-to-end.

    Returns:
        True on success, False if data or training failed.
    """
    trainer = ChestXRayTrainer(img_size=img_size, batch_size=batch_size)

    train_gen, val_gen, test_gen = trainer.create_data_generators()
    if train_gen is None:
        logger.error(
            "Cannot start training – processed data not found.\n"
            "Run:  python backend/scripts/create_balanced_dataset.py"
        )
        return False

    trainer.build_model()
    trainer.train_model(train_gen, val_gen, epochs=epochs)
    trainer.plot_training_history()
    accuracy, report, _ = trainer.evaluate_model(test_gen)

    final_path = Path(settings.models_dir) / "final_chest_xray_model.h5"
    trainer.model.save(str(final_path))
    logger.info("Final model saved → %s", final_path)
    logger.info("Training pipeline complete | accuracy=%.1f%%", accuracy * 100)
    return True

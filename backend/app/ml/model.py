"""
backend/app/ml/model.py

Model loading, preprocessing, and inference helpers.

All ML computations are **identical** to the original api/main.py logic; this
module simply wraps them in a clean, testable class and makes the model a
module-level singleton that the FastAPI lifespan loads once.

Architecture: MobileNetV2 fine-tuned for binary chest X-ray classification.
Input:  224×224 RGB, normalised to [0, 1] (rescale=1./255).
Output: scalar sigmoid probability (>0.5 → PNEUMONIA, ≤0.5 → NORMAL).
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Suppress TF C++ logs at import time (must happen before `import tensorflow`)
# ---------------------------------------------------------------------------
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import tensorflow as tf  # noqa: E402  (intentional late import after env var)


# ---------------------------------------------------------------------------
# Module-level singleton state
# ---------------------------------------------------------------------------
_model: Optional[tf.keras.Model] = None
_model_meta: dict = {
    "loaded": False,
    "load_time": None,
    "model_path": None,
}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def get_model() -> Optional[tf.keras.Model]:
    """Return the loaded Keras model, or None if not yet loaded."""
    return _model


def get_model_meta() -> dict:
    """Return a copy of the current model metadata dict."""
    return dict(_model_meta)


def load_model() -> bool:
    """
    Discover and load the Keras model from the configured search paths.

    The function populates the module-level ``_model`` and ``_model_meta``
    singletons.  It is called once during the FastAPI lifespan startup.

    Returns:
        True if the model was loaded successfully, False otherwise.
    """
    global _model, _model_meta

    # Build ordered list of candidate paths
    candidates: list[Path] = []

    # 1. Explicit override takes absolute priority
    if settings.model_path_override:
        candidates.append(Path(settings.model_path_override))

    # 2. Configured search paths
    candidates.extend(Path(p) for p in settings.model_search_paths)

    for candidate in candidates:
        if candidate.exists():
            logger.info("Loading model from: %s", candidate)
            try:
                _model = tf.keras.models.load_model(str(candidate))
                _model_meta = {
                    "loaded": True,
                    "load_time": datetime.now().isoformat(),
                    "model_path": str(candidate),
                }
                logger.info("✅ Model loaded successfully from %s", candidate)
                return True
            except Exception as exc:
                logger.error("Failed to load model from %s: %s", candidate, exc)
                # Try next candidate
                continue

    logger.error(
        "❌ Model file not found. Searched paths:\n%s",
        "\n".join(f"  • {p}" for p in candidates),
    )
    return False


# ---------------------------------------------------------------------------
# Preprocessing  (must match training preprocessing in scripts/train_model.py)
# ---------------------------------------------------------------------------

def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Preprocess a PIL Image for MobileNetV2 inference.

    Steps (identical to training pipeline):
      1. Convert to RGB if needed.
      2. Resize to (IMG_SIZE × IMG_SIZE) – bilinear by default.
      3. Cast to float32 and normalise to [0, 1].
      4. Add batch dimension → shape (1, IMG_SIZE, IMG_SIZE, 3).

    Args:
        image: PIL Image of any mode or size.

    Returns:
        NumPy array of shape (1, 224, 224, 3), dtype float32.
    """
    size = settings.model_input_size

    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize((size, size), resample=Image.BILINEAR)
    img_array = np.array(image, dtype=np.float32) / 255.0   # → [0, 1]
    img_array = np.expand_dims(img_array, axis=0)            # → (1, H, W, C)
    return img_array


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

def run_inference(image: Image.Image) -> dict:
    """
    Full inference pipeline: preprocess → predict → interpret.

    Args:
        image: A PIL Image (any size/mode; preprocessing handles conversion).

    Returns:
        A dict with keys:
          - diagnosis        : "PNEUMONIA" | "NORMAL"
          - confidence       : float (0–100)
          - confidence_level : "Low" | "Moderate" | "High"
          - recommendation   : str
          - raw_score        : float (0–1, raw sigmoid output)

    Raises:
        RuntimeError: If the model is not loaded.
        ValueError:   If the model returns an unexpected output shape.
    """
    model = get_model()
    if model is None:
        raise RuntimeError(
            "Model is not loaded. The server may still be starting up, "
            "or the model file could not be found."
        )

    processed = preprocess_image(image)
    raw_output = model.predict(processed, verbose=0)

    # Handle both scalar and 2-D outputs gracefully
    if raw_output.ndim == 2:
        prediction_score = float(raw_output[0][0])
    elif raw_output.ndim == 1:
        prediction_score = float(raw_output[0])
    else:
        raise ValueError(
            f"Unexpected model output shape: {raw_output.shape}. "
            "Expected a scalar sigmoid output."
        )

    return interpret_prediction(prediction_score)


def interpret_prediction(prediction_score: float) -> dict:
    """
    Map a raw sigmoid score to a structured result dict.

    Threshold and confidence tier logic are **unchanged** from the original
    api/main.py ``interpret_prediction`` function.

    Args:
        prediction_score: Raw sigmoid output in [0, 1].
                          >0.5 → PNEUMONIA, ≤0.5 → NORMAL.

    Returns:
        dict with keys: diagnosis, confidence, confidence_level,
                        recommendation, raw_score.
    """
    threshold = settings.prediction_threshold

    if prediction_score > threshold:
        diagnosis = "PNEUMONIA"
        confidence = float(prediction_score * 100)

        if confidence >= 80:
            confidence_level = "High"
            recommendation = (
                "Strong indication of pneumonia. "
                "Recommend immediate medical attention."
            )
        elif confidence >= 60:
            confidence_level = "Moderate"
            recommendation = (
                "Moderate indication of pneumonia. "
                "Medical review recommended."
            )
        else:
            confidence_level = "Low"
            recommendation = (
                "Possible pneumonia detected. "
                "Further examination advised."
            )
    else:
        diagnosis = "NORMAL"
        confidence = float((1.0 - prediction_score) * 100)

        if confidence >= 80:
            confidence_level = "High"
            recommendation = "No signs of pneumonia detected. Chest X-ray appears normal."
        elif confidence >= 60:
            confidence_level = "Moderate"
            recommendation = (
                "Likely normal chest X-ray. "
                "Routine follow-up if symptoms persist."
            )
        else:
            confidence_level = "Low"
            recommendation = (
                "Unclear result. Manual review by radiologist recommended."
            )

    return {
        "diagnosis": diagnosis,
        "confidence": round(confidence, 2),
        "confidence_level": confidence_level,
        "recommendation": recommendation,
        "raw_score": round(prediction_score, 6),
    }

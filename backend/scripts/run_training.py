"""
backend/scripts/run_training.py

CLI entry point for training the MobileNetV2 chest X-ray classifier.

Usage (from backend/ directory):
    python scripts/run_training.py
    python scripts/run_training.py --epochs 30 --batch-size 16
    python scripts/run_training.py --img-size 224 --epochs 25
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Make sure `backend/` is on the Python path when running as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.logging import setup_logging
from app.ml.training import run_training_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train the PneumoDetectAI MobileNetV2 model."
    )
    parser.add_argument(
        "--img-size", type=int, default=224,
        help="Input image size in pixels (default: 224)."
    )
    parser.add_argument(
        "--batch-size", type=int, default=32,
        help="Training batch size (default: 32)."
    )
    parser.add_argument(
        "--epochs", type=int, default=25,
        help="Maximum number of training epochs (default: 25)."
    )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(level=args.log_level)
    logger = logging.getLogger(__name__)

    logger.info(
        "Starting training | img_size=%d | batch=%d | epochs=%d",
        args.img_size, args.batch_size, args.epochs,
    )

    success = run_training_pipeline(
        img_size=args.img_size,
        batch_size=args.batch_size,
        epochs=args.epochs,
    )

    if success:
        logger.info("✅ Training pipeline completed successfully.")
        sys.exit(0)
    else:
        logger.error("❌ Training pipeline failed. Check logs above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()

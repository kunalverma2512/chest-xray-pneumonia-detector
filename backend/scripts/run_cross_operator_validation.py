#!/usr/bin/env python3
"""
backend/scripts/run_cross_operator_validation.py

CLI entry point for cross-operator validation against an independent dataset.

Usage (from project root):
    python backend/scripts/run_cross_operator_validation.py \\
        --dataset-path data/raw/external_validation

The external validation dataset must have:
    dataset-path/
        NORMAL/       (JPEG/PNG images)
        PNEUMONIA/    (JPEG/PNG images)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.logging import setup_logging
from app.ml.evaluation import CrossOperatorValidator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run cross-operator validation on an independent dataset."
    )
    parser.add_argument(
        "--dataset-path", required=True,
        help="Path to dataset directory with NORMAL/ and PNEUMONIA/ sub-folders."
    )
    parser.add_argument(
        "--model-path", default=None,
        help="Path to the .h5 model file. Defaults to models/best_chest_xray_model.h5."
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Where to save results. Defaults to results/cross-operator_validation/."
    )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(level=args.log_level)
    logger = logging.getLogger(__name__)

    validator = CrossOperatorValidator(
        model_path=args.model_path,
        dataset_path=args.dataset_path,
        output_dir=args.output_dir,
    )

    try:
        metrics = validator.run()
        logger.info("\n" + "=" * 55)
        logger.info("  CROSS-OPERATOR VALIDATION RESULTS")
        logger.info("=" * 55)
        logger.info("  Accuracy      : %.1f%%", metrics["cross_operator_accuracy"] * 100)
        logger.info("  Sensitivity   : %.1f%%", metrics["cross_operator_sensitivity"] * 100)
        logger.info("  Specificity   : %.1f%%", metrics["cross_operator_specificity"] * 100)
        logger.info("  Samples       : %d", metrics["cross_operator_samples"])
        logger.info("  Accuracy drop : %.1f%%", metrics["accuracy_drop"] * 100)
        logger.info("=" * 55)
        logger.info(
            "✅ Validation complete. Results saved to results/cross-operator_validation/"
        )
        sys.exit(0)
    except Exception as e:
        logger.error("❌ Cross-operator validation failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()

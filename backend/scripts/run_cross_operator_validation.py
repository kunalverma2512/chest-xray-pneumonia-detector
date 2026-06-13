"""
backend/scripts/run_cross_operator_validation.py

CLI entry point for cross-operator validation.

Usage (from backend/ directory):
    python scripts/run_cross_operator_validation.py \\
        --dataset-path /path/to/cross_operator_validation_dataset/test

The dataset directory must contain NORMAL/ and PNEUMONIA/ sub-folders.
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
        description="Run cross-operator validation for PneumoDetectAI."
    )
    parser.add_argument(
        "--dataset-path", required=True,
        help="Path to the cross-operator validation dataset directory. "
             "Must contain NORMAL/ and PNEUMONIA/ sub-folders."
    )
    parser.add_argument(
        "--model-path", default=None,
        help="Explicit path to the .h5 model file. "
             "Defaults to the path from settings."
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Directory to write results and visualisations. "
             "Defaults to results/cross-operator_validation/."
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
        output_dir=args.output_dir,
    )

    try:
        results = validator.run(dataset_path=args.dataset_path)
    except Exception as exc:
        logger.error("Cross-operator validation failed: %s", exc)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("CROSS-OPERATOR VALIDATION RESULTS")
    print("=" * 60)
    for key, value in results.items():
        print(f"  {key:<45} {value}")
    print("=" * 60)


if __name__ == "__main__":
    main()

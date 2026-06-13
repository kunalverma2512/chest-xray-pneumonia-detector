"""
backend/scripts/run_evaluation.py

CLI entry point for evaluating the model on the internal test set.

Usage (from backend/ directory):
    python scripts/run_evaluation.py
    python scripts/run_evaluation.py --model-path /path/to/model.h5
    python scripts/run_evaluation.py --data-path /path/to/processed
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.logging import setup_logging
from app.ml.evaluation import ModelEvaluator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate PneumoDetectAI on the internal test set."
    )
    parser.add_argument(
        "--model-path", default=None,
        help="Explicit path to the .h5 model file. "
             "Defaults to the path from settings."
    )
    parser.add_argument(
        "--data-path", default=None,
        help="Path to the processed dataset directory (must contain a test/ folder). "
             "Defaults to the path from settings."
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="Skip saving the JSON metrics file."
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

    evaluator = ModelEvaluator(
        model_path=args.model_path,
        data_path=args.data_path,
    )

    try:
        metrics = evaluator.run(save_json=not args.no_save)
    except Exception as exc:
        logger.error("Evaluation failed: %s", exc)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    for key, value in metrics.items():
        if key != "confusion_matrix":
            print(f"  {key:<30} {value}")
    print("=" * 60)


if __name__ == "__main__":
    main()

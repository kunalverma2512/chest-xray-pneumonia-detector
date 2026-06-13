#!/usr/bin/env python3
"""
backend/scripts/run_evaluation.py

CLI entry point for evaluating the trained model on the internal test set.

Usage (from project root):
    python backend/scripts/run_evaluation.py
    python backend/scripts/run_evaluation.py --model-path models/best_chest_xray_model.h5
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
        description="Evaluate the PneumoDetectAI model on the internal test set."
    )
    parser.add_argument(
        "--model-path", default=None,
        help="Path to the .h5 model file. Defaults to models/best_chest_xray_model.h5."
    )
    parser.add_argument(
        "--data-path", default=None,
        help="Path to the processed data directory. Defaults to data/processed/."
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
        metrics = evaluator.run()
        logger.info("\n" + "=" * 55)
        logger.info("  INTERNAL EVALUATION RESULTS")
        logger.info("=" * 55)
        logger.info("  Accuracy      : %.1f%%", metrics["accuracy"] * 100)
        logger.info("  Sensitivity   : %.1f%%", metrics["sensitivity"] * 100)
        logger.info("  Specificity   : %.1f%%", metrics["specificity"] * 100)
        logger.info("  F1-Score      : %.4f", metrics["f1_score"])
        logger.info("  ROC-AUC       : %.4f", metrics["roc_auc"])
        logger.info("=" * 55)
        logger.info("✅ Evaluation complete. Results saved to results/internal_validation/")
        sys.exit(0)
    except Exception as e:
        logger.error("❌ Evaluation failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()

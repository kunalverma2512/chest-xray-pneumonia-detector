"""
backend/app/api/v1/endpoints/health.py

Health-check and model-info endpoints.

Routes:
  GET /api/v1/health   – liveness / readiness probe
  GET /api/v1/info     – detailed model metadata
  GET /api/v1/stats    – performance metrics from cross-operator validation
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter

from app.core.config import settings
from app.ml.model import get_model_meta
from app.schemas.inference import (
    ConfusionMatrixStats,
    HealthResponse,
    ModelInfoResponse,
    ModelPerformanceStats,
    StatsResponse,
)

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="API health check",
    description=(
        "Returns the operational status of the API and whether the ML model "
        "is loaded and ready to serve predictions."
    ),
)
def health_check() -> HealthResponse:
    meta = get_model_meta()
    status = "healthy" if meta["loaded"] else "unhealthy"
    return HealthResponse(
        status=status,
        model_loaded=meta["loaded"],
        model_path=meta.get("model_path"),
        load_time=meta.get("load_time"),
        timestamp=datetime.now().isoformat(),
        performance_summary=(
            f"{settings.xval_accuracy:.0f}% accuracy, "
            f"{settings.xval_sensitivity:.1f}% sensitivity, "
            f"{settings.xval_false_positive_rate:.1f}% false positive rate"
        ),
    )


@router.get(
    "/info",
    response_model=ModelInfoResponse,
    summary="Detailed model information",
    description="Returns architecture details, clinical validation metrics, and usage guidelines.",
)
def model_info() -> ModelInfoResponse:
    meta = get_model_meta()
    return ModelInfoResponse(
        model_loaded=meta["loaded"],
        model_path=meta.get("model_path"),
        load_time=meta.get("load_time"),
        clinical_validation={
            "accuracy": f"{settings.xval_accuracy:.1f}%",
            "sensitivity": f"{settings.xval_sensitivity:.1f}%",
            "specificity": f"{settings.xval_specificity:.1f}%",
            "clinical_readiness": "READY for clinical validation",
        },
        cross_operator_validation={
            "dataset_size": "485 independent samples",
            "normal_cases": "234",
            "pneumonia_cases": "251",
            "generalization": "Good (8.8% drop from internal validation)",
        },
        technical_specs={
            "architecture": "MobileNetV2 with custom classification head",
            "input_size": f"{settings.model_input_size}x{settings.model_input_size} RGB images",
            "training_data": "Balanced dataset (1:1 ratio)",
            "preprocessing": (
                f"Resize to {settings.model_input_size}x{settings.model_input_size}, "
                "normalise to [0, 1]"
            ),
            "prediction_threshold": settings.prediction_threshold,
        },
        usage_guidelines={
            "intended_use": "Preliminary pneumonia screening assistant",
            "limitations": "Not a replacement for professional diagnosis",
            "recommendation": "Always consult healthcare professionals for medical decisions",
        },
    )


@router.get(
    "/stats",
    response_model=StatsResponse,
    summary="Cross-operator validation performance statistics",
    description="Returns the full confusion matrix and performance metrics from cross-operator validation.",
)
def get_stats() -> StatsResponse:
    return StatsResponse(
        performance_metrics=ModelPerformanceStats(
            overall_accuracy=f"{settings.xval_accuracy:.1f}%",
            sensitivity=f"{settings.xval_sensitivity:.1f}%",
            specificity=f"{settings.xval_specificity:.1f}%",
            precision="80.4%",
            false_positive_rate=f"{settings.xval_false_positive_rate:.1f}%",
            false_negative_rate="3.6%",
            roc_auc=str(settings.xval_roc_auc),
            pr_auc=str(settings.xval_pr_auc),
        ),
        cross_operator_validation_confusion_matrix=ConfusionMatrixStats(
            true_negatives=175,
            false_positives=59,
            false_negatives=9,
            true_positives=242,
            total_test_samples=485,
        ),
        clinical_interpretation={
            "excellent_screening": (
                f"{settings.xval_sensitivity:.1f}% sensitivity ideal for pneumonia screening"
            ),
            "false_alarm_consideration": (
                f"{settings.xval_false_positive_rate:.1f}% false positive rate requires clinical review"
            ),
            "high_detection_rate": (
                f"{settings.xval_sensitivity:.1f}% of pneumonia cases correctly identified"
            ),
            "clinical_readiness": "Ready for real-world clinical validation",
        },
        validation_methodology={
            "type": "cross_operator_validation",
            "dataset": settings.xval_validated_on,
            "generalization": "Good (8.8% drop from internal validation)",
        },
    )

"""
backend/app/schemas/inference.py

Pydantic request / response models for the prediction endpoint.

These are the canonical data contracts between the FastAPI backend and any
frontend consumer (React + Vite, Swagger UI, automated tests, etc.).
"""

from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Nested sub-models
# ---------------------------------------------------------------------------

class ExternalValidationPerformance(BaseModel):
    """Baked-in cross-operator validation metrics from the published paper."""

    accuracy: str = Field(
        ...,
        description="Overall accuracy on the external validation set.",
        examples=["86.0%"],
    )
    sensitivity: str = Field(
        ...,
        description="Sensitivity (True Positive Rate) on the external validation set.",
        examples=["96.4%"],
    )
    specificity: str = Field(
        ...,
        description="Specificity (True Negative Rate) on the external validation set.",
        examples=["74.8%"],
    )
    validated_on: str = Field(
        ...,
        description="Description of the validation cohort.",
        examples=["485 independent samples"],
    )


class ModelPerformanceStats(BaseModel):
    """Detailed model performance breakdown returned by /api/v1/health and /api/v1/info."""

    overall_accuracy: str
    sensitivity: str
    specificity: str
    precision: str
    false_positive_rate: str
    false_negative_rate: str
    roc_auc: str
    pr_auc: str


class ConfusionMatrixStats(BaseModel):
    true_negatives: int
    false_positives: int
    false_negatives: int
    true_positives: int
    total_test_samples: int


# ---------------------------------------------------------------------------
# Prediction endpoint – response
# ---------------------------------------------------------------------------

class PredictionResponse(BaseModel):
    """
    JSON response returned by `POST /api/v1/predict`.

    All fields are designed for direct consumption by a React frontend.
    """
    model_config = ConfigDict(protected_namespaces=())

    # Core result
    diagnosis: Literal["PNEUMONIA", "NORMAL"] = Field(
        ...,
        description="Binary diagnosis label.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Confidence score as a percentage (0–100).",
        examples=[94.3],
    )
    confidence_level: Literal["Low", "Moderate", "High"] = Field(
        ...,
        description="Human-readable confidence tier.",
    )
    raw_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Raw sigmoid output from the model (0–1).",
    )

    # Contextual metadata
    recommendation: str = Field(
        ...,
        description="Clinical recommendation string based on the diagnosis and confidence.",
    )
    external_validation_performance: ExternalValidationPerformance = Field(
        ...,
        description="Cross-operator validation metrics for transparency.",
    )
    disclaimer: str = Field(
        default=(
            "This AI assistant is for preliminary screening only. "
            "Always consult healthcare professionals for medical decisions."
        ),
    )

    # Request echo
    filename: Optional[str] = Field(
        default=None,
        description="Name of the uploaded file.",
    )
    image_size: Optional[str] = Field(
        default=None,
        description="Original image dimensions as '{width}x{height}'.",
    )
    timestamp: str = Field(
        ...,
        description="ISO-8601 timestamp of the inference.",
    )


# ---------------------------------------------------------------------------
# Health endpoint – response
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    """JSON response for `GET /api/v1/health`."""
    model_config = ConfigDict(protected_namespaces=())

    status: Literal["healthy", "degraded", "unhealthy"]
    model_loaded: bool
    model_path: Optional[str] = None
    load_time: Optional[str] = None
    timestamp: str
    performance_summary: str = Field(
        default="86% accuracy, 96.4% sensitivity, 25.2% false positive rate",
    )


# ---------------------------------------------------------------------------
# Info endpoint – response
# ---------------------------------------------------------------------------

class ModelInfoResponse(BaseModel):
    """JSON response for `GET /api/v1/info`."""
    model_config = ConfigDict(protected_namespaces=())

    model_loaded: bool
    model_path: Optional[str]
    load_time: Optional[str]
    clinical_validation: dict
    cross_operator_validation: dict
    technical_specs: dict
    usage_guidelines: dict


# ---------------------------------------------------------------------------
# Stats endpoint – response
# ---------------------------------------------------------------------------

class StatsResponse(BaseModel):
    """JSON response for `GET /api/v1/stats`."""

    performance_metrics: ModelPerformanceStats
    cross_operator_validation_confusion_matrix: ConfusionMatrixStats
    clinical_interpretation: dict
    validation_methodology: dict

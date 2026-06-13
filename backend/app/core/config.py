"""
backend/app/core/config.py

Centralised application settings.

All values can be overridden via environment variables or a `.env` file placed
in the `backend/` directory.  Pydantic-Settings reads them automatically.

Usage anywhere in the app:
    from app.core.config import settings
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------------------------------
# Resolve the repo root so we can derive default paths robustly regardless of
# where uvicorn is launched from.
# ---------------------------------------------------------------------------
# backend/app/core/config.py  →  go up 3 levels → backend/
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
# backend/ → project root
_PROJECT_ROOT = _BACKEND_DIR.parent


class Settings(BaseSettings):
    """Application-wide configuration."""

    model_config = SettingsConfigDict(
        # Look for a `.env` file in the backend/ directory
        env_file=str(_BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # API metadata
    # ------------------------------------------------------------------
    app_title: str = "PneumoDetectAI - Pediatric Pneumonia Detection API"
    app_description: str = (
        "Clinical-grade AI pneumonia screening: "
        "86% cross-operator validation accuracy, "
        "96.4% sensitivity (485 samples)."
    )
    app_version: str = "2.0.0"
    api_v1_prefix: str = "/api/v1"

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "info"

    # ------------------------------------------------------------------
    # CORS – list additional origins as a comma-separated env var, e.g.
    #   CORS_ORIGINS="http://localhost:5173,https://your-prod.vercel.app"
    # ------------------------------------------------------------------
    cors_origins: List[str] = [
        "http://localhost:5173",   # Vite default dev port
        "http://127.0.0.1:5173",
        "http://localhost:3000",   # CRA / other common ports
        "http://127.0.0.1:3000",
    ]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | List[str]) -> List[str]:
        """Accept either a Python list or a comma-separated string from env."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    # ------------------------------------------------------------------
    # Model paths
    # The loader in ml/model.py will try these in order until one exists.
    # ------------------------------------------------------------------
    model_search_paths: List[str] = [
        # Committed / downloaded weight inside the old api folder
        str(_PROJECT_ROOT / "api" / "streamlit_api_folder" / "best_chest_xray_model.h5"),
        # Canonical training output location
        str(_PROJECT_ROOT / "models" / "best_chest_xray_model.h5"),
        # Backend-local copy (useful when deploying backend in isolation)
        str(_BACKEND_DIR / "models" / "best_chest_xray_model.h5"),
    ]

    # Override with a single absolute path if you know exactly where it is
    model_path_override: str = ""

    # ------------------------------------------------------------------
    # ML / inference constants  (must match training preprocessing)
    # ------------------------------------------------------------------
    model_input_size: int = 224          # px – MobileNetV2 default
    prediction_threshold: float = 0.5   # >threshold → PNEUMONIA
    max_upload_size_mb: int = 10         # Hard limit on uploaded image size

    # ------------------------------------------------------------------
    # Cross-operator validation ground-truth metrics (baked in from paper)
    # ------------------------------------------------------------------
    xval_accuracy: float = 86.0
    xval_sensitivity: float = 96.4
    xval_specificity: float = 74.8
    xval_false_positive_rate: float = 25.2
    xval_roc_auc: float = 0.964
    xval_pr_auc: float = 0.968
    xval_validated_on: str = "485 independent samples"

    # ------------------------------------------------------------------
    # Data paths (used by training / evaluation scripts)
    # ------------------------------------------------------------------
    data_root: str = str(_PROJECT_ROOT / "data")
    processed_data_dir: str = str(_PROJECT_ROOT / "data" / "processed")
    raw_data_dir: str = str(_PROJECT_ROOT / "data" / "raw")
    models_dir: str = str(_PROJECT_ROOT / "models")
    results_dir: str = str(_PROJECT_ROOT / "results")

    # ------------------------------------------------------------------
    # Training hyper-parameters (matched to existing train_model.py)
    # ------------------------------------------------------------------
    train_img_size: int = 224
    train_batch_size: int = 32
    train_epochs: int = 25
    train_learning_rate: float = 0.001


# Module-level singleton – import this everywhere
settings = Settings()

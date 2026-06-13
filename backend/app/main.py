"""
backend/app/main.py

FastAPI application entry point.

Responsibilities:
  1. Create the FastAPI app instance with metadata from settings.
  2. Register CORS middleware (configured for React + Vite dev server).
  3. Mount the v1 API router under /api/v1.
  4. Lifespan: load the ML model on startup, release on shutdown.
  5. Register global exception handlers for 404 / 500.
  6. Expose a root GET / for liveness probes and quick API info.

Running:
  cd backend/
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.ml.model import load_model, get_model_meta

# Configure logging before anything else imports a logger
setup_logging(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan (replaces deprecated @app.on_event)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Startup:  Load the Keras model into the module-level singleton.
    Shutdown: Log a clean exit (model GC'd automatically).
    """
    logger.info("⏳ Starting PneumoDetectAI API…")
    success = load_model()
    if success:
        meta = get_model_meta()
        logger.info(
            "✅ Model ready | path=%s | loaded_at=%s",
            meta["model_path"],
            meta["load_time"],
        )
    else:
        logger.warning(
            "⚠️  Model could not be loaded. "
            "POST /api/v1/predict will return 503 until the model is available. "
            "Set MODEL_PATH_OVERRIDE env var or place the .h5 file in one of the "
            "configured search paths."
        )

    yield  # ← application runs here

    logger.info("🛑 PneumoDetectAI API shutting down.")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ---------------------------------------------------------------- CORS
    # In production, replace or narrow `cors_origins` via the CORS_ORIGINS env var.
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # ---------------------------------------------------------- API routes
    application.include_router(api_router, prefix=settings.api_v1_prefix)

    # ---------------------------------------------------- exception handlers
    @application.exception_handler(404)
    async def not_found_handler(request: Request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Endpoint not found.",
                "hint": "Visit /docs for the interactive API documentation.",
            },
        )

    @application.exception_handler(500)
    async def internal_error_handler(request: Request, exc) -> JSONResponse:
        logger.error("Unhandled 500 error: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error. Please try again or contact support."
            },
        )

    # ---------------------------------------------------------- root probe
    @application.get(
        "/",
        tags=["root"],
        summary="API root – liveness probe",
        include_in_schema=True,
    )
    def root() -> dict:
        meta = get_model_meta()
        return {
            "service": "PneumoDetectAI",
            "version": settings.app_version,
            "status": "running",
            "model_loaded": meta["loaded"],
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "health": f"{settings.api_v1_prefix}/health",
                "predict": f"{settings.api_v1_prefix}/predict",
                "info": f"{settings.api_v1_prefix}/info",
                "stats": f"{settings.api_v1_prefix}/stats",
                "docs": "/docs",
            },
        }

    return application


# Module-level app instance (used by uvicorn)
app = create_app()

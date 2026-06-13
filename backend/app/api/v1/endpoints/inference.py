"""
backend/app/api/v1/endpoints/inference.py

Prediction endpoint for chest X-ray pneumonia detection.

Route:
  POST /api/v1/predict
    - Accepts:  multipart/form-data with a single `file` field.
    - Returns:  JSON conforming to PredictionResponse schema.

Design notes:
  - Uses async file reading for non-blocking I/O.
  - All ML work is synchronous (tf.keras.Model.predict) but runs in a thread
    pool via run_in_executor to avoid blocking the event loop.
  - Returns clean JSON only – no HTML, no server-side rendering.
"""

from __future__ import annotations

import logging
from datetime import datetime
from functools import partial

import anyio
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from app.core.config import settings
from app.ml.model import get_model, run_inference
from app.schemas.inference import ExternalValidationPerformance, PredictionResponse
from app.utils.io import read_image_bytes, validate_upload, image_size_str

logger = logging.getLogger(__name__)

router = APIRouter(tags=["inference"])


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict pneumonia from a chest X-ray image",
    description=(
        "Upload a chest X-ray image (JPEG / PNG / WebP) as multipart/form-data. "
        "Returns a JSON object with the AI diagnosis, confidence score, "
        "confidence tier, clinical recommendation, and cross-operator "
        "validation metrics for transparency.\n\n"
        "**Disclaimer**: For preliminary screening only. "
        "Always consult a qualified healthcare professional."
    ),
    responses={
        200: {"description": "Successful prediction"},
        400: {"description": "Invalid image file or content type"},
        413: {"description": "File too large (max 10 MB)"},
        503: {"description": "Model not yet loaded"},
    },
)
async def predict_pneumonia(
    file: UploadFile = File(
        ...,
        description="Chest X-ray image file (JPEG, PNG, or WebP). Max 10 MB.",
    ),
) -> PredictionResponse:
    """
    End-to-end inference pipeline:

    1. Validate content-type and file size.
    2. Read bytes asynchronously.
    3. Decode PIL Image (via utils/io.py).
    4. Run model inference in a thread pool (avoids blocking event loop).
    5. Build and return a PredictionResponse.
    """

    # ------------------------------------------------------------------ guard
    if get_model() is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Model is not loaded. The server may still be starting up. "
                "Try again in a few seconds, or check /api/v1/health."
            ),
        )

    # --------------------------------------------------------- validate upload
    validate_upload(
        content_type=file.content_type,
        file_size_bytes=getattr(file, "size", None),
        max_size_mb=settings.max_upload_size_mb,
    )

    # ---------------------------------------------------------- read raw bytes
    try:
        raw_bytes = await file.read()
    except Exception as exc:
        logger.error("Failed to read uploaded file '%s': %s", file.filename, exc)
        raise HTTPException(
            status_code=400,
            detail="Could not read the uploaded file.",
        ) from exc
    finally:
        await file.close()

    # -------------------------------------------------- size guard (post-read)
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(raw_bytes) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(raw_bytes) / 1_048_576:.1f} MB). "
                   f"Maximum allowed size is {settings.max_upload_size_mb} MB.",
        )

    # ------------------------------------------------------------ decode image
    image = read_image_bytes(raw_bytes, filename=file.filename or "<upload>")
    original_size = image_size_str(image)
    logger.info(
        "Processing '%s' | size=%s | mode=%s",
        file.filename,
        original_size,
        image.mode,
    )

    # ----------------------------------------------------- run model (in pool)
    try:
        result = await run_in_threadpool(run_inference, image)
    except RuntimeError as exc:
        # Model not loaded (race condition guard)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Inference failed for '%s'", file.filename)
        raise HTTPException(
            status_code=500,
            detail=f"Inference error: {exc}",
        ) from exc

    logger.info(
        "Prediction complete | file='%s' | diagnosis=%s | confidence=%.1f%%",
        file.filename,
        result["diagnosis"],
        result["confidence"],
    )

    # --------------------------------------------------------- build response
    return PredictionResponse(
        diagnosis=result["diagnosis"],
        confidence=result["confidence"],
        confidence_level=result["confidence_level"],
        raw_score=result["raw_score"],
        recommendation=result["recommendation"],
        external_validation_performance=ExternalValidationPerformance(
            accuracy=f"{settings.xval_accuracy:.1f}%",
            sensitivity=f"{settings.xval_sensitivity:.1f}%",
            specificity=f"{settings.xval_specificity:.1f}%",
            validated_on=settings.xval_validated_on,
        ),
        filename=file.filename,
        image_size=original_size,
        timestamp=datetime.now().isoformat(),
    )

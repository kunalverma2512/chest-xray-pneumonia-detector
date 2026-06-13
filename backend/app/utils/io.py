"""
backend/app/utils/io.py

Common I/O helpers shared across the application.
"""

from __future__ import annotations

import io
import logging
from typing import Tuple

from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException

logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/bmp",
    "image/tiff",
}


def read_image_bytes(raw_bytes: bytes, filename: str = "<upload>") -> Image.Image:
    """
    Open raw bytes as a PIL Image, with validation.

    Args:
        raw_bytes: The raw file bytes from an uploaded multipart field.
        filename:  Original filename (for error messages only).

    Returns:
        A PIL Image object in RGB mode.

    Raises:
        HTTPException 400 if the bytes cannot be decoded as an image.
    """
    try:
        image = Image.open(io.BytesIO(raw_bytes))
        image.verify()  # Detects truncated / corrupt images
    except (UnidentifiedImageError, Exception) as exc:
        logger.warning("Failed to open image '%s': %s", filename, exc)
        raise HTTPException(
            status_code=400,
            detail=f"Could not decode image '{filename}'. "
                   "Please upload a valid JPEG, PNG, or WebP file.",
        ) from exc

    # Re-open after verify() (verify() closes the file pointer internally)
    image = Image.open(io.BytesIO(raw_bytes))

    if image.mode != "RGB":
        image = image.convert("RGB")

    return image


def validate_upload(
    content_type: str | None,
    file_size_bytes: int | None,
    max_size_mb: int = 10,
) -> None:
    """
    Validate content-type and file size before processing.

    Raises:
        HTTPException 400 for bad content-type or oversize files.
    """
    if not content_type or content_type not in ALLOWED_CONTENT_TYPES:
        # Be permissive if content_type is None (some clients don't send it)
        if content_type is not None:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported file type '{content_type}'. "
                    f"Accepted types: {', '.join(sorted(ALLOWED_CONTENT_TYPES))}."
                ),
            )

    max_bytes = max_size_mb * 1024 * 1024
    if file_size_bytes is not None and file_size_bytes > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {max_size_mb} MB.",
        )


def image_size_str(image: Image.Image) -> str:
    """Return image dimensions as a '{width}x{height}' string."""
    w, h = image.size
    return f"{w}x{h}"

"""
backend/tests/test_inference.py

Unit tests for the core ML and API inference logic.

Run from the backend/ directory:
    pytest tests/ -v
    pytest tests/test_inference.py -v --tb=short

These tests do NOT require the model .h5 file to be present –
they mock the ML layer and test the preprocessing / interpretation logic.
"""

from __future__ import annotations

import io
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from PIL import Image

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_rgb_image(width: int = 300, height: int = 400) -> Image.Image:
    """Create a random RGB PIL Image for testing."""
    rng = np.random.default_rng(42)
    data = (rng.random((height, width, 3)) * 255).astype(np.uint8)
    return Image.fromarray(data, mode="RGB")


def _make_greyscale_image(width: int = 256, height: int = 256) -> Image.Image:
    rng = np.random.default_rng(7)
    data = (rng.random((height, width)) * 255).astype(np.uint8)
    return Image.fromarray(data, mode="L")


def _image_to_bytes(image: Image.Image, fmt: str = "JPEG") -> bytes:
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# preprocess_image
# ---------------------------------------------------------------------------

class TestPreprocessImage:
    def test_output_shape(self):
        from app.ml.model import preprocess_image

        img = _make_rgb_image(300, 400)
        result = preprocess_image(img)
        assert result.shape == (1, 224, 224, 3)

    def test_normalisation_range(self):
        from app.ml.model import preprocess_image

        img = _make_rgb_image(300, 300)
        result = preprocess_image(img)
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_dtype_is_float32(self):
        from app.ml.model import preprocess_image

        img = _make_rgb_image()
        result = preprocess_image(img)
        assert result.dtype == np.float32

    def test_grayscale_converted_to_rgb(self):
        from app.ml.model import preprocess_image

        grey = _make_greyscale_image()
        result = preprocess_image(grey)
        # Should still produce (1, 224, 224, 3)
        assert result.shape == (1, 224, 224, 3)


# ---------------------------------------------------------------------------
# interpret_prediction
# ---------------------------------------------------------------------------

class TestInterpretPrediction:
    def test_pneumonia_high_confidence(self):
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.95)
        assert result["diagnosis"] == "PNEUMONIA"
        assert result["confidence_level"] == "High"
        assert result["confidence"] == pytest.approx(95.0, abs=0.1)

    def test_pneumonia_moderate_confidence(self):
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.65)
        assert result["diagnosis"] == "PNEUMONIA"
        assert result["confidence_level"] == "Moderate"

    def test_pneumonia_low_confidence(self):
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.55)
        assert result["diagnosis"] == "PNEUMONIA"
        assert result["confidence_level"] == "Low"

    def test_normal_high_confidence(self):
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.05)
        assert result["diagnosis"] == "NORMAL"
        assert result["confidence_level"] == "High"
        assert result["confidence"] == pytest.approx(95.0, abs=0.1)

    def test_normal_moderate_confidence(self):
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.35)
        assert result["diagnosis"] == "NORMAL"
        assert result["confidence_level"] == "Moderate"

    def test_normal_low_confidence(self):
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.45)
        assert result["diagnosis"] == "NORMAL"
        assert result["confidence_level"] == "Low"

    def test_exact_threshold_is_normal(self):
        """Score exactly at threshold (0.5) should be NORMAL."""
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.5)
        assert result["diagnosis"] == "NORMAL"

    def test_raw_score_preserved(self):
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.7777)
        assert result["raw_score"] == pytest.approx(0.7777, abs=1e-4)

    def test_keys_present(self):
        from app.ml.model import interpret_prediction

        result = interpret_prediction(0.8)
        assert set(result.keys()) == {
            "diagnosis", "confidence", "confidence_level",
            "recommendation", "raw_score"
        }


# ---------------------------------------------------------------------------
# utils/io.py
# ---------------------------------------------------------------------------

class TestValidateUpload:
    def test_rejects_unsupported_content_type(self):
        from fastapi import HTTPException
        from app.utils.io import validate_upload

        with pytest.raises(HTTPException) as exc_info:
            validate_upload(content_type="application/pdf", file_size_bytes=None)
        assert exc_info.value.status_code == 400

    def test_accepts_jpeg(self):
        from app.utils.io import validate_upload

        # Should not raise
        validate_upload(content_type="image/jpeg", file_size_bytes=100_000)

    def test_rejects_oversized_file(self):
        from fastapi import HTTPException
        from app.utils.io import validate_upload

        with pytest.raises(HTTPException) as exc_info:
            validate_upload(
                content_type="image/jpeg",
                file_size_bytes=20 * 1024 * 1024,  # 20 MB
                max_size_mb=10,
            )
        assert exc_info.value.status_code == 413

    def test_passes_none_content_type(self):
        """None content-type (some old clients) should not raise."""
        from app.utils.io import validate_upload

        validate_upload(content_type=None, file_size_bytes=500_000)


class TestReadImageBytes:
    def test_valid_jpeg(self):
        from app.utils.io import read_image_bytes

        img = _make_rgb_image()
        raw = _image_to_bytes(img, "JPEG")
        result = read_image_bytes(raw, "test.jpg")
        assert result.mode == "RGB"

    def test_valid_png(self):
        from app.utils.io import read_image_bytes

        img = _make_rgb_image()
        raw = _image_to_bytes(img, "PNG")
        result = read_image_bytes(raw, "test.png")
        assert result.mode == "RGB"

    def test_invalid_bytes_raises_400(self):
        from fastapi import HTTPException
        from app.utils.io import read_image_bytes

        with pytest.raises(HTTPException) as exc_info:
            read_image_bytes(b"not an image", "bad.jpg")
        assert exc_info.value.status_code == 400

    def test_greyscale_converted_to_rgb(self):
        from app.utils.io import read_image_bytes

        grey = _make_greyscale_image()
        raw = _image_to_bytes(grey, "PNG")
        result = read_image_bytes(raw, "grey.png")
        assert result.mode == "RGB"

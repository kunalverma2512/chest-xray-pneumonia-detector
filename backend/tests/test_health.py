"""
backend/tests/test_health.py

Integration-style tests for the health and stats endpoints.
Uses FastAPI's TestClient – does NOT load the actual TF model.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """Provide a TestClient with the model patched to 'not loaded'."""
    from app.main import app
    return TestClient(app, raise_server_exceptions=True)


class TestRootEndpoint:
    def test_root_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_root_has_expected_keys(self, client):
        data = client.get("/").json()
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert "endpoints" in data


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200

    def test_health_schema(self, client):
        data = client.get("/api/v1/health").json()
        assert "status" in data
        assert "model_loaded" in data
        assert "timestamp" in data

    def test_health_status_unhealthy_when_no_model(self, client):
        with patch("app.api.v1.endpoints.health.get_model_meta") as mock:
            mock.return_value = {"loaded": False, "model_path": None, "load_time": None}
            data = client.get("/api/v1/health").json()
        assert data["status"] == "unhealthy"
        assert data["model_loaded"] is False


class TestStatsEndpoint:
    def test_stats_returns_200(self, client):
        resp = client.get("/api/v1/stats")
        assert resp.status_code == 200

    def test_stats_has_performance_metrics(self, client):
        data = client.get("/api/v1/stats").json()
        assert "performance_metrics" in data
        assert "cross_operator_validation_confusion_matrix" in data


class TestInfoEndpoint:
    def test_info_returns_200(self, client):
        resp = client.get("/api/v1/info")
        assert resp.status_code == 200

    def test_info_has_required_sections(self, client):
        data = client.get("/api/v1/info").json()
        assert "technical_specs" in data
        assert "clinical_validation" in data
        assert "usage_guidelines" in data


class TestNotFound:
    def test_unknown_route_returns_404(self, client):
        resp = client.get("/api/v1/does-not-exist")
        assert resp.status_code == 404
        data = resp.json()
        assert "detail" in data

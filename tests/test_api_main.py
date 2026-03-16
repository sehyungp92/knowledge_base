"""Tests for FastAPI application setup."""

from unittest.mock import patch, MagicMock

import pytest


def test_health_endpoint():
    with patch("webapp.api.main.init_pool"), \
         patch("webapp.api.main.close_pool"):
        from webapp.api.main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"


def test_cors_allows_localhost():
    with patch("webapp.api.main.init_pool"), \
         patch("webapp.api.main.close_pool"):
        from webapp.api.main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        resp = client.get("/api/health", headers={"Origin": "http://localhost:3000"})
        assert resp.status_code == 200

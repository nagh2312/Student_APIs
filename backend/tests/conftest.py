"""pytest configuration and fixtures."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

# Force mock mode for tests before app import
os.environ["MOCK_MODE"] = "true"
os.environ["API_KEY_PEPPER"] = "test-pepper"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"


@pytest.fixture(scope="session")
def client():
    from app.main import create_app

    app = create_app()
    with TestClient(app) as c:
        yield c

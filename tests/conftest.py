"""
MediCore Nexus - Pytest Configuration and Test Fixtures
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


@pytest.fixture(scope="session")
def client():
    """Test client for invoking FastAPI endpoints."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def auth_headers(client):
    """Obtain valid JWT authorization headers for testing."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "admin@medicorenexus.io", "password": "Admin@12345"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

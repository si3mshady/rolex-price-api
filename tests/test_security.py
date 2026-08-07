from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)


def test_api_key_disabled_by_default():
    """Verify that when API_KEY_REQUIRED is False, endpoints are accessible without X-Api-Key."""
    settings.API_KEY_REQUIRED = False
    response = client.get("/watches")
    assert response.status_code == 200


def test_api_key_required_missing_header():
    """Verify 401 Unauthorized when API_KEY_REQUIRED is True and header is missing."""
    settings.API_KEY_REQUIRED = True
    response = client.get("/watches")
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "UNAUTHORIZED"
    settings.API_KEY_REQUIRED = False


def test_api_key_required_invalid_header():
    """Verify 401 Unauthorized when invalid key is provided."""
    settings.API_KEY_REQUIRED = True
    response = client.get("/watches", headers={"X-Api-Key": "wrong-key"})
    assert response.status_code == 401
    settings.API_KEY_REQUIRED = False


def test_api_key_required_valid_header():
    """Verify 200 OK when valid X-Api-Key is provided."""
    settings.API_KEY_REQUIRED = True
    response = client.get("/watches", headers={"X-Api-Key": settings.API_KEY})
    assert response.status_code == 200
    settings.API_KEY_REQUIRED = False


def test_health_endpoint_remains_public():
    """Verify that /health endpoint is always accessible regardless of API_KEY_REQUIRED setting."""
    settings.API_KEY_REQUIRED = True
    response = client.get("/health")
    assert response.status_code == 200
    settings.API_KEY_REQUIRED = False

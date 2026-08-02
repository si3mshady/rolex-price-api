from fastapi import status
from fastapi.testclient import TestClient
from app.schemas.health import HealthResponse


def test_get_health_success(client: TestClient):
    """
    Test GET /health returns HTTP 200 and matches HealthResponse schema.
    """
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "Rolex Price API"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data
    assert data["watches_loaded"] == 10

    # Validate response schema with Pydantic model
    validated = HealthResponse.model_validate(data)
    assert validated.watches_loaded == 10


def test_get_health_real_catalog(real_catalog_client: TestClient):
    """
    Test GET /health returns actual catalog count when running against real data.
    """
    response = real_catalog_client.get("/health")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "healthy"
    assert data["watches_loaded"] > 0

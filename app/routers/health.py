from fastapi import APIRouter, status
from app.schemas.health import HealthResponse
from app.services.rolex_service import rolex_service

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="API Health Check",
    description="Returns the health status, application version, timestamp, and count of loaded Rolex watches.",
)
async def get_health() -> HealthResponse:
    """
    Check the health and operational status of the service.
    """
    return rolex_service.get_health_status()

from fastapi import APIRouter, status
from app.schemas.statistics import StatisticsResponse
from app.services.rolex_service import rolex_service

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get(
    "",
    response_model=StatisticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Rolex Catalog Statistics",
    description="Calculates catalog-wide summary analytics, price & size metrics, collection distributions, and top priced watch highlights.",
)
async def get_statistics() -> StatisticsResponse:
    """
    Get comprehensive catalog statistics.
    """
    return rolex_service.get_statistics()

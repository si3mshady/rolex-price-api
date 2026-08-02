from fastapi import APIRouter, Query, status
from app.schemas.collection import CollectionListResponse
from app.services.rolex_service import rolex_service

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get(
    "",
    response_model=CollectionListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Rolex Collections",
    description="Retrieves a summary of all Rolex collection families, including model counts, price ranges, sizes, and complications.",
)
async def list_collections(
    sort_by: str = Query("name", pattern="^(name|watch_count|avg_price)$", description="Field to sort collections by"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort direction ('asc' or 'desc')"),
) -> CollectionListResponse:
    """
    Get breakdown of all Rolex collection families.
    """
    return rolex_service.get_collections(sort_by=sort_by, sort_order=sort_order)

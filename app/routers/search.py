from typing import Optional
from fastapi import APIRouter, Query, HTTPException, status
from app.schemas.watch import PaginatedWatchResponse
from app.services.rolex_service import rolex_service

router = APIRouter(prefix="/search", tags=["Search"])


@router.get(
    "",
    response_model=PaginatedWatchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search Rolex Catalog",
    description="Performs keyword search across reference numbers, collection names, dial descriptions, and complications with optional filters.",
)
async def search_watches(
    q: str = Query(..., min_length=1, description="Search query string"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Items per page limit"),
    collection: Optional[str] = Query(None, description="Optional collection filter"),
    min_price: Optional[float] = Query(
        None, ge=0, description="Optional minimum price filter"
    ),
    max_price: Optional[float] = Query(
        None, ge=0, description="Optional maximum price filter"
    ),
) -> PaginatedWatchResponse:
    """
    Search Rolex catalog by text query.
    """
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price.",
        )

    return rolex_service.search_watches(
        q=q,
        page=page,
        limit=limit,
        collection=collection,
        min_price=min_price,
        max_price=max_price,
    )

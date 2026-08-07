from typing import Optional
from fastapi import APIRouter, Query, Path, HTTPException, status
from app.schemas.watch import PaginatedWatchResponse, WatchReferenceDetailResponse
from app.schemas.error import ErrorResponse
from app.services.rolex_service import rolex_service, RolexNotFoundError

router = APIRouter(prefix="/watches", tags=["Watches"])


@router.get(
    "",
    response_model=PaginatedWatchResponse,
    status_code=status.HTTP_200_OK,
    summary="List Rolex Watches",
    description="Retrieves a paginated list of Rolex watches with flexible filtering and sorting parameters.",
)
async def list_watches(
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Number of items per page limit"),
    collection: Optional[str] = Query(
        None, description="Filter by collection name (case-insensitive)"
    ),
    min_price: Optional[float] = Query(
        None, ge=0, description="Minimum retail price filter"
    ),
    max_price: Optional[float] = Query(
        None, ge=0, description="Maximum retail price filter"
    ),
    min_size: Optional[int] = Query(
        None, ge=0, description="Minimum watch case size (mm)"
    ),
    max_size: Optional[int] = Query(
        None, ge=0, description="Maximum watch case size (mm)"
    ),
    complication: Optional[str] = Query(
        None, description="Filter by watch complication"
    ),
    is_por: Optional[bool] = Query(
        None, description="Filter by Price On Request status"
    ),
    sort_by: str = Query(
        "reference",
        pattern="^(reference|collection|price|size)$",
        description="Field to sort by",
    ),
    sort_order: str = Query(
        "asc", pattern="^(asc|desc)$", description="Sort direction ('asc' or 'desc')"
    ),
) -> PaginatedWatchResponse:
    """
    Get paginated watches catalog.
    """
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price.",
        )

    if min_size is not None and max_size is not None and min_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_size cannot be greater than max_size.",
        )

    return rolex_service.get_watches(
        collection=collection,
        min_price=min_price,
        max_price=max_price,
        min_size=min_size,
        max_size=max_size,
        complication=complication,
        is_por=is_por,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )


@router.get(
    "/{reference}",
    response_model=WatchReferenceDetailResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Watch reference not found",
        }
    },
    summary="Get Rolex Watch Reference Details",
    description="Retrieves details and dial/finish variants for a specific Rolex reference number.",
)
async def get_watch_by_reference(
    reference: str = Path(
        ..., description="Rolex watch reference number (e.g., '116500LN')"
    ),
) -> WatchReferenceDetailResponse:
    """
    Get watch details by reference number.
    """
    try:
        return rolex_service.get_watch_by_reference(reference)
    except RolexNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )

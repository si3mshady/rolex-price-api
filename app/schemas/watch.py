from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class WatchSchema(BaseModel):
    """
    Schema representing detailed Rolex watch information.
    """

    id: str = Field(
        ..., description="Unique watch item identifier", example="watch-001-116900"
    )
    reference: str = Field(
        ..., description="Rolex reference number", example="116500LN"
    )
    collection: str = Field(
        ..., description="Rolex collection family", example="Cosmograph Daytona"
    )
    description: str = Field(
        ..., description="Dial or finish description", example="Standard Dial"
    )
    size: int = Field(..., description="Case size diameter in mm", example=40)
    rrp: str = Field(
        ...,
        description="Recommended Retail Price string as cataloged",
        example="12600.0",
    )
    price: Optional[float] = Field(
        None,
        description="Parsed numeric retail price, or null if Price On Request",
        example=12600.0,
    )
    is_por: bool = Field(
        False, description="True if price is Price On Request (POR)", example=False
    )
    complications: List[str] = Field(
        default_factory=list,
        description="List of watch complications",
        example=["Chronograph", "Small Seconds"],
    )

    model_config = ConfigDict(from_attributes=True)


class PaginatedWatchResponse(BaseModel):
    """
    Paginated response container for watch listings.
    """

    total: int = Field(..., description="Total number of matching watches", example=895)
    page: int = Field(..., description="Current page number", example=1)
    limit: int = Field(..., description="Number of items per page limit", example=20)
    total_pages: int = Field(..., description="Total pages available", example=45)
    items: List[WatchSchema] = Field(
        ..., description="List of watches for current page"
    )


class WatchReferenceDetailResponse(BaseModel):
    """
    Detailed response for a specific watch reference lookup.
    """

    reference: str = Field(..., description="Rolex reference number", example="116503")
    collection: str = Field(
        ..., description="Collection family name", example="Cosmograph Daytona"
    )
    variants_count: int = Field(
        ...,
        description="Number of dial/finish variants found for this reference",
        example=3,
    )
    min_price: Optional[float] = Field(
        None, description="Lowest price among variants for this reference"
    )
    max_price: Optional[float] = Field(
        None, description="Highest price among variants for this reference"
    )
    variants: List[WatchSchema] = Field(
        ..., description="All watch variants under this reference number"
    )

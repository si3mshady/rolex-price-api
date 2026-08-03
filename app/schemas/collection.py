from typing import List, Optional
from pydantic import BaseModel, Field


class CollectionSummary(BaseModel):
    """
    Summary breakdown of a single Rolex collection family.
    """
    name: str = Field(..., description="Collection name", example="Cosmograph Daytona")
    watch_count: int = Field(..., description="Total watches in this collection", example=9)
    min_price: Optional[float] = Field(None, description="Lowest priced watch in collection", example=12600.0)
    max_price: Optional[float] = Field(None, description="Highest priced watch in collection", example=78840.0)
    avg_price: Optional[float] = Field(None, description="Average watch price in collection", example=37000.0)
    sizes: List[int] = Field(..., description="Available watch case sizes (mm) in this collection", example=[40])
    complications: List[str] = Field(..., description="Unique watch complications present in collection", example=["Chronograph", "Small Seconds"])


class CollectionListResponse(BaseModel):
    """
    Response model for listing all Rolex collections.
    """
    total_collections: int = Field(..., description="Total number of collections", example=17)
    collections: List[CollectionSummary] = Field(..., description="List of collection summaries")

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.schemas.watch import WatchSchema


class PriceStatistics(BaseModel):
    """
    Statistical metrics on retail watch prices.
    """
    total_priced_watches: int = Field(..., description="Number of watches with explicit numeric pricing", example=729)
    total_por_watches: int = Field(..., description="Number of watches listed as Price On Request (POR)", example=166)
    min_price: Optional[float] = Field(None, description="Minimum retail price in dataset", example=5700.0)
    max_price: Optional[float] = Field(None, description="Maximum retail price in dataset", example=114000.0)
    avg_price: Optional[float] = Field(None, description="Average retail price across priced watches", example=21500.0)
    median_price: Optional[float] = Field(None, description="Median retail price across priced watches", example=14500.0)


class SizeStatistics(BaseModel):
    """
    Statistical metrics on watch sizes.
    """
    min_size: int = Field(..., description="Smallest watch size diameter (mm)", example=28)
    max_size: int = Field(..., description="Largest watch size diameter (mm)", example=44)
    avg_size: float = Field(..., description="Average watch size diameter (mm)", example=37.5)
    size_distribution: Dict[int, int] = Field(..., description="Map of watch size (mm) to count of models", example={40: 150, 36: 120})


class StatisticsResponse(BaseModel):
    """
    Comprehensive statistics response model for the Rolex catalog.
    """
    total_watches: int = Field(..., description="Total watch records cataloged", example=895)
    total_unique_references: int = Field(..., description="Total unique reference numbers", example=171)
    total_collections: int = Field(..., description="Total unique collection families", example=17)
    price_stats: PriceStatistics = Field(..., description="Price distribution statistics")
    size_stats: SizeStatistics = Field(..., description="Size distribution statistics")
    collection_counts: Dict[str, int] = Field(..., description="Count of watches per collection family")
    complication_counts: Dict[str, int] = Field(..., description="Count of watches per complication type")
    most_expensive_watches: List[WatchSchema] = Field(..., description="Top highest priced watch models")
    least_expensive_watches: List[WatchSchema] = Field(..., description="Top lowest priced watch models")

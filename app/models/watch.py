from typing import List, Optional
from pydantic import BaseModel, Field


class Watch(BaseModel):
    """
    Domain model representing a Rolex watch item.
    """

    id: str = Field(..., description="Unique internal identifier for the watch item")
    reference: str = Field(..., description="Rolex watch reference number")
    collection: str = Field(..., description="Rolex collection family name")
    description: str = Field(..., description="Watch dial and aesthetic description")
    size: int = Field(..., description="Watch case diameter in millimeters (mm)")
    rrp: str = Field(..., description="Original Recommended Retail Price string")
    price: Optional[float] = Field(
        None,
        description="Parsed numeric price in USD/currency, null if Price On Request",
    )
    is_por: bool = Field(
        False, description="Flag indicating if price is Price On Request (POR)"
    )
    complications: List[str] = Field(
        default_factory=list, description="List of watch complications"
    )

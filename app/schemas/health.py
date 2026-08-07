from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Response model for the /health check endpoint.
    """

    status: str = Field(
        "healthy", description="Current status of the API", example="healthy"
    )
    app_name: str = Field(
        ..., description="Application name", example="Rolex Price API"
    )
    version: str = Field(..., description="API Version", example="1.0.0")
    timestamp: datetime = Field(..., description="Current server UTC timestamp")
    watches_loaded: int = Field(
        ..., description="Number of watches currently loaded in memory", example=895
    )

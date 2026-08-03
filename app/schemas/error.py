from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """
    Detailed information about an API error response.
    """
    code: str = Field(..., description="Machine-readable error code", example="NOT_FOUND")
    message: str = Field(..., description="Human-readable error description", example="Rolex reference '116500LN' was not found.")
    details: Optional[Dict[str, Any]] = Field(None, description="Optional diagnostic or validation details")


class ErrorResponse(BaseModel):
    """
    Standardized API error response container.
    """
    error: ErrorDetail

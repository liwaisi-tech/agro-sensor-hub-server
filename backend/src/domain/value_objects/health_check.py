from datetime import datetime, UTC
from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    """
    Value object representing a health check status.
    This is immutable and defined by its attributes.
    """
    status: str = Field(
        ...,
        description="Current health status of the system"   
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp of the last health check"
    )

    class Config:
        frozen = True  # Makes the model immutable
        json_schema_extra = {
            "example": {
                "status": "ok",
                "timestamp": "2024-03-08T12:00:00Z"
            }
        } 
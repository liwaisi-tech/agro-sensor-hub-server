from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field, StringConstraints

class DeviceBase(BaseModel):
    """Base Pydantic model for Device data."""
    mac_address: Annotated[
        str, 
        StringConstraints(pattern=r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$')
    ] = Field(description="Device MAC address in format XX:XX:XX:XX:XX:XX")
    
    name: Optional[Annotated[
        str, 
        StringConstraints(min_length=1, max_length=100)
    ]] = Field(default=None, description="Device name (optional)")

class DeviceCreate(DeviceBase):
    """Pydantic model for creating a new Device."""
    pass

class DeviceResponse(DeviceBase):
    """Pydantic model for Device responses including timestamps."""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model to Pydantic model

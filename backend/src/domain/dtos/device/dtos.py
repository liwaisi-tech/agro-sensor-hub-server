from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field, StringConstraints

class DeviceBase(BaseModel):
    """Base Pydantic model for Device data."""
    mac_address: Annotated[
        str, 
        StringConstraints(pattern=r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$')
    ] = Field(
        title="MAC Address",
        description="Device MAC address in format XX:XX:XX:XX:XX:XX",
        examples=["35:98:f4:d1:86:51"]
    )
    
    name: Optional[Annotated[
        str, 
        StringConstraints(min_length=1, max_length=100)
    ]] = Field(
        default=None,
        title="Device Name",
        description="Device name (optional)",
        examples=["AgroSensor-Elite-2024"]
    )

class DeviceCreate(DeviceBase):
    """Pydantic model for creating a new Device."""
    class Config:
        json_schema_extra = {
            "example": {
                "mac_address": "35:98:f4:d1:86:51",
                "name": "AgroSensor-Elite-2024"
            }
        }

class DeviceResponse(DeviceBase):
    """Pydantic model for Device responses including timestamps."""
    created_at: datetime = Field(
        title="Created At",
        description="Timestamp when the device was created",
        examples=["2024-03-09T14:11:36.387495Z"]
    )
    updated_at: datetime = Field(
        title="Updated At",
        description="Timestamp when the device was last updated",
        examples=["2024-03-09T14:15:51.893824Z"]
    )

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model to Pydantic model
        json_schema_extra = {
            "example": {
                "mac_address": "35:98:f4:d1:86:51",
                "name": "AgroSensor-Elite-2024",
                "created_at": "2024-03-09T14:11:36.387495Z",
                "updated_at": "2024-03-09T14:15:51.893824Z"
            }
        }

from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field, StringConstraints


class SensorActivityBase(BaseModel):
    """Base Pydantic model for Sensor Activity data."""

    mac_address: Annotated[
        str, StringConstraints(pattern=r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    ] = Field(
        title="MAC Address",
        description="Device MAC address in format XX:XX:XX:XX:XX:XX",
        examples=["35:98:f4:d1:86:51"],
    )
    zone: Optional[str] = Field(
        default=None,
        title="Zone",
        description="Zone where the sensor is located",
        examples=["Zone A"],
    )
    env_humidity: Optional[float] = Field(
        default=None,
        title="Environmental Humidity",
        description="Environmental humidity reading",
        ge=0,
        le=100,
        examples=[65.5],
    )
    env_temperature: Optional[float] = Field(
        default=None,
        title="Environmental Temperature",
        description="Environmental temperature reading in Celsius",
        examples=[25.3],
    )
    ground_sensor_1: Optional[float] = Field(
        default=None,
        title="Ground Sensor 1",
        description="Ground sensor 1 reading",
        examples=[500],
    )
    ground_sensor_2: Optional[float] = Field(
        default=None,
        title="Ground Sensor 2",
        description="Ground sensor 2 reading",
        examples=[520],
    )
    ground_sensor_3: Optional[float] = Field(
        default=None,
        title="Ground Sensor 3",
        description="Ground sensor 3 reading",
        examples=[480],
    )
    ground_sensor_4: Optional[float] = Field(
        default=None,
        title="Ground Sensor 4",
        description="Ground sensor 4 reading",
        examples=[510],
    )
    ground_sensor_5: Optional[float] = Field(
        default=None,
        title="Ground Sensor 5",
        description="Ground sensor 5 reading",
        examples=[490],
    )
    ground_sensor_6: Optional[float] = Field(
        default=None,
        title="Ground Sensor 6",
        description="Ground sensor 6 reading",
        examples=[505],
    )


class SensorActivityCreate(SensorActivityBase):
    """Pydantic model for creating a new Sensor Activity."""

    class Config:
        json_schema_extra = {
            "example": {
                "mac_address": "35:98:f4:d1:86:51",
                "zone": "Zone A",
                "env_humidity": 65.5,
                "env_temperature": 25.3,
                "ground_sensor_1": 500,
                "ground_sensor_2": 520,
                "ground_sensor_3": 480,
                "ground_sensor_4": 510,
                "ground_sensor_5": 490,
                "ground_sensor_6": 505,
            }
        }


class SensorActivityResponse(BaseModel):
    """Pydantic model for Sensor Activity responses including timestamps and ID."""

    id: int = Field(
        title="ID", description="Unique identifier for the sensor activity record"
    )
    mac_address: Annotated[
        str, StringConstraints(pattern=r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    ] = Field(
        title="MAC Address",
        description="Device MAC address in format XX:XX:XX:XX:XX:XX",
        examples=["35:98:f4:d1:86:51"],
        alias="device_id",
    )
    zone: Optional[str] = None
    env_humidity: Optional[float] = None
    env_temperature: Optional[float] = None
    ground_sensor_1: Optional[float] = None
    ground_sensor_2: Optional[float] = None
    ground_sensor_3: Optional[float] = None
    ground_sensor_4: Optional[float] = None
    ground_sensor_5: Optional[float] = None
    ground_sensor_6: Optional[float] = None
    created_at: datetime = Field(
        title="Created At",
        description="Timestamp when the sensor activity was recorded",
        examples=["2024-03-09T14:11:36.387495Z"],
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "mac_address": "35:98:f4:d1:86:51",
                "zone": "Zone A",
                "env_humidity": 65.5,
                "env_temperature": 25.3,
                "ground_sensor_1": 500,
                "ground_sensor_2": 520,
                "ground_sensor_3": 480,
                "ground_sensor_4": 510,
                "ground_sensor_5": 490,
                "ground_sensor_6": 505,
                "created_at": "2024-03-09T14:11:36.387495Z",
            }
        }

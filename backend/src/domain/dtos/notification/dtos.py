from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    """Base DTO for notification data."""

    device_id: str = Field(..., description="The MAC address of the device")
    type: str = Field(..., description="Type of notification")
    title: str = Field(..., description="Title of the notification")
    description: Optional[str] = Field(
        None, description="Optional description of the notification"
    )


class NotificationCreate(NotificationBase):
    """DTO for creating a new notification."""

    pass


class NotificationResponse(NotificationBase):
    """DTO for notification responses."""

    id: int = Field(..., description="The unique identifier of the notification")
    is_read: bool = Field(..., description="Whether the notification has been read")
    created_at: datetime = Field(..., description="When the notification was created")
    updated_at: datetime = Field(
        ..., description="When the notification was last updated"
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True

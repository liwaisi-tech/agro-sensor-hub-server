from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from infrastructure.database.base import Base


class Device(Base):
    """Model for registering ESP32 devices by MAC address."""

    __tablename__ = "devices"

    mac_address = Column(String(17), primary_key=True)  # Format: XX:XX:XX:XX:XX:XX
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    sensor_activities = relationship("SensorActivity", back_populates="device")

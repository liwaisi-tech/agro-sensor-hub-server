from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func

from infrastructure.database.base import Base

class Notification(Base):
    """Model for storing system notifications."""
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(17), ForeignKey('devices.mac_address'), nullable=False)
    type = Column(String(50), nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 
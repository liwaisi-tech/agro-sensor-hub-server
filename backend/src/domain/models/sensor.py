from sqlalchemy import Column, Integer, String, Float, DateTime, func
from infrastructure.database.base import Base

class Sensor(Base):
    """
    Sensor model representing a physical sensor in the system.
    """
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    location = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 
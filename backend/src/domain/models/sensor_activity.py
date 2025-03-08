from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from infrastructure.database.base import Base

class SensorActivity(Base):
    """Model for storing sensor activity data from ESP32 devices."""
    __tablename__ = 'sensor_activities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mac_address = Column(String(17), nullable=False, index=True)  # Format: XX:XX:XX:XX:XX:XX
    zone = Column(String(100), nullable=True)
    env_humidity = Column(Float, nullable=True)
    env_temperature = Column(Float, nullable=True)
    ground_sensor_1 = Column(Float, nullable=True)
    ground_sensor_2 = Column(Float, nullable=True)
    ground_sensor_3 = Column(Float, nullable=True)
    ground_sensor_4 = Column(Float, nullable=True)
    ground_sensor_5 = Column(Float, nullable=True)
    ground_sensor_6 = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

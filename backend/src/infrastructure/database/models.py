from domain.models.sensor_activity import SensorActivity
from domain.models.device import Device
from domain.models.notification import Notification

# Import all models here to ensure they are registered with SQLAlchemy
__all__ = ['SensorActivity', 'Device', 'Notification'] 
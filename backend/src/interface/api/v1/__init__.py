from .health import router as health_router
from .device import router as device_router
from .sensor_activity.controller import router as sensor_activity_router
from .notification.controller import router as notification_router

__all__ = [
    "health_router",
    "device_router",
    "sensor_activity_router",
    "notification_router",
]

from fastapi import APIRouter
from .v1 import (
    health_router,
    device_router,
    sensor_activity_router,
    notification_router,
)

# Create main API router
api_router = APIRouter()

# Include domain-specific routers
api_router.include_router(health_router, prefix="/v1")
api_router.include_router(device_router, prefix="/v1")
api_router.include_router(sensor_activity_router, prefix="/v1")
api_router.include_router(notification_router, prefix="/v1")
__all__ = ["api_router"]

from fastapi import APIRouter
from .v1 import health_router

# Create main API router
api_router = APIRouter()

# Include domain-specific routers
api_router.include_router(health_router, prefix="/v1")

__all__ = ['api_router'] 
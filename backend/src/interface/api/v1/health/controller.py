from fastapi import APIRouter
from domain.value_objects.health_check import HealthCheck

router = APIRouter(
    prefix="/health",
    tags=["Health Check"]
)

@router.get(
    "",
    response_model=HealthCheck,
    summary="Health Check endpoint",
    description="Returns the current health status of the system"
)
async def health_check() -> HealthCheck:
    """
    Health check endpoint that returns the current status of the system.
    
    Returns:
        HealthCheck: A value object containing the health status and timestamp
    """
    return HealthCheck(status="ok") 
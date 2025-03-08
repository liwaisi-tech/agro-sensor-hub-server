from fastapi import APIRouter
from domain.value_objects.health_check import HealthCheck
from application.services.health.health_service import HealthService
from fastapi import Depends

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
async def health_check(health_service: HealthService = Depends(HealthService)) -> HealthCheck:
    """
    Health check endpoint that returns the current status of the system.
    
    Args:
        health_service: Service that handles health check logic
    
    Returns:
        HealthCheck: A value object containing the health status and timestamp
    """
    health_status = health_service.get_health()
    return HealthCheck(status=health_status["status"]) 
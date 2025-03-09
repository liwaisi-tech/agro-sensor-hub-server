from fastapi import APIRouter
from domain.value_objects.health_check import HealthCheck
from application.services.health.health_service import HealthService
from fastapi import Depends
from infrastructure.logging_config import get_logger

logger = get_logger(__name__)

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
    logger.info("Health check endpoint called")
    health_status = health_service.get_health()
    logger.info(f"Health check response: {health_status}")
    return HealthCheck(status=health_status["status"]) 
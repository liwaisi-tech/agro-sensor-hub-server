from infrastructure.logging_config import get_logger

logger = get_logger(__name__)

class HealthService:
    def __init__(self):
        pass

    def get_health(self):
        """
        Get the health status of the system.
        
        Returns:
            dict: A dictionary containing the health status
        """
        logger.debug("Checking system health")
        health_status = {"status": "ok"}
        logger.debug(f"System health status: {health_status}")
        return health_status
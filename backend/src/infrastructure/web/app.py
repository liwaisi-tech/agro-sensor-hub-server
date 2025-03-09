from fastapi import FastAPI, Request
from interface.api import api_router
from infrastructure.config.settings import get_settings
from infrastructure.logging_config import get_logger
import time

logger = get_logger(__name__)

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application instance
    """
    settings = get_settings()
    logger.info("Creating FastAPI application")
    
    app = FastAPI(
        title="Agro Sensor Hub API",
        description="API for managing agricultural sensors and their data",
        version="1.0.0",
        docs_url="/docs",  # Set Swagger UI path
        redoc_url="/redoc",  # Set ReDoc path
        openapi_url="/openapi.json"  # Set OpenAPI schema path
    )
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all requests with their processing time."""
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} "
            f"Process Time: {process_time:.2f}ms"
        )
        return response
    
    # Include API router
    logger.info(f"Configuring API router with prefix: {settings.API_PREFIX}")
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    return app

# Create the application instance
app = create_app()
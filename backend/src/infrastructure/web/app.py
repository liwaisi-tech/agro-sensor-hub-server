from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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
    prefix = settings.API_PREFIX.strip()  # Remove any trailing spaces
    logger.info("Creating FastAPI application")

    app = FastAPI(
        title="Agro Sensor Hub API",
        description="API for managing agricultural sensors and their data",
        version="1.0.0",
        docs_url=f"{prefix}/docs",  # Include API prefix in Swagger UI path
        redoc_url=f"{prefix}/redoc",  # Include API prefix in ReDoc path
        openapi_url=f"{prefix}/openapi.json",  # Include API prefix in OpenAPI schema path
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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

    # Include API router with the API prefix
    logger.info(f"Configuring API router with prefix: {prefix}")
    app.include_router(api_router, prefix=prefix)

    return app


# Create the application instance
app = create_app()

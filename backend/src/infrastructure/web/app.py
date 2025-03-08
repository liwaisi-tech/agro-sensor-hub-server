from fastapi import FastAPI
from interface.api import api_router
from infrastructure.config.settings import get_settings

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application instance
    """
    settings = get_settings()
    app = FastAPI(
        title="Agro Sensor Hub API",
        description="API for managing agricultural sensors and their data",
        version="1.0.0",
    )
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    return app

# Create the application instance
app = create_app() 
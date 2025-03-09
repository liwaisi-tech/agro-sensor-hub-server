import uvicorn
from typing import Any
from infrastructure.logging_config import get_logger, ColorFormatter
import logging

logger = get_logger(__name__)

def start_server(host: str = "0.0.0.0", 
                port: int = 8080, 
                reload: bool = False,
                **kwargs: Any) -> None:
    """
    Starts the uvicorn server with the FastAPI application.
    
    Args:
        host (str): Host to bind to
        port (int): Port to bind to
        reload (bool): Enable auto-reload
        **kwargs: Additional uvicorn server options
    """
    logger.info(f"Starting server on {host}:{port}")
    
    # Configure Uvicorn logging to use our format
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "()": ColorFormatter,
                "fmt": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            }
        },
        "handlers": {
            "default": {
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False
            }
        }
    }
    
    uvicorn.run(
        "infrastructure.web.app:app",
        host=host,
        port=port,
        reload=reload,
        log_config=log_config,
        access_log=True,
        **kwargs
    ) 
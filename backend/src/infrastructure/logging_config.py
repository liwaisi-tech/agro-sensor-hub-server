import logging
import logging.config
import sys
from typing import Dict, Any
from infrastructure.config.settings import get_settings

# ANSI color codes
COLORS = {
    "GREY": "\033[38;21m",
    "BLUE": "\033[34m",
    "YELLOW": "\033[33m",
    "RED": "\033[31m",
    "BOLD_RED": "\033[31;1m",
    "GREEN": "\033[32m",
    "RESET": "\033[0m",
}


class ColorFormatter(logging.Formatter):
    """Custom formatter that adds colors based on log level"""

    def __init__(self, fmt: str):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: COLORS["BLUE"] + fmt + COLORS["RESET"],
            logging.INFO: COLORS["GREEN"] + fmt + COLORS["RESET"],
            logging.WARNING: COLORS["YELLOW"] + fmt + COLORS["RESET"],
            logging.ERROR: COLORS["RED"] + fmt + COLORS["RESET"],
            logging.CRITICAL: COLORS["BOLD_RED"] + fmt + COLORS["RESET"],
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger_config() -> Dict[str, Any]:
    """Returns the logging configuration dictionary"""
    settings = get_settings()
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "()": ColorFormatter,
                "fmt": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "standard",
                "stream": sys.stdout,
            }
        },
        "loggers": {
            "domain": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "application": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "infrastructure": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "interface": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "alembic": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "alembic.runtime.migration": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
        },
        "root": {"level": settings.LOG_LEVEL, "handlers": ["console"]},
    }


def setup_logging():
    """Initialize logging configuration"""
    settings = get_settings()
    config = get_logger_config()
    logging.config.dictConfig(config)

    # Force SQLAlchemy and Alembic loggers to use our formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        ColorFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    console_handler.setLevel(settings.LOG_LEVEL)

    # Update SQLAlchemy loggers
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.handlers = [console_handler]
    sqlalchemy_logger.setLevel(settings.LOG_LEVEL)

    # Update Alembic loggers
    alembic_logger = logging.getLogger("alembic")
    alembic_logger.handlers = [console_handler]
    alembic_logger.setLevel(settings.LOG_LEVEL)
    alembic_migration_logger = logging.getLogger("alembic.runtime.migration")
    alembic_migration_logger.handlers = [console_handler]
    alembic_migration_logger.setLevel(settings.LOG_LEVEL)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the specified name

    Args:
        name: The name of the logger, typically the module name

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)

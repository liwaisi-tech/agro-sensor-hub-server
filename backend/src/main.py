import subprocess
import sys
import os
from pathlib import Path
from infrastructure.web import start_server
from infrastructure.logging_config import setup_logging, get_logger
from infrastructure.config.settings import get_settings

# Change to the project root directory
os.chdir(Path(__file__).parent.parent)

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Test loggers for each namespace
domain_logger = get_logger("domain")
app_logger = get_logger("application")
infra_logger = get_logger("infrastructure")
interface_logger = get_logger("interface")


def run_migrations():
    """
    Run database migrations using Alembic.
    """
    try:
        logger.info("Starting database migrations")
        # Set environment variables for Alembic logging
        env = os.environ.copy()
        env["PYTHONPATH"] = str(
            Path(__file__).parent.parent
        )  # Set PYTHONPATH to include our src directory
        env["ALEMBIC_LOG_FORMAT"] = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        env["ALEMBIC_LOG_LEVEL"] = "INFO"

        # Ensure settings are loaded before migrations
        settings = get_settings()
        env.update(
            {
                "POSTGRES_USER": settings.POSTGRES_USER,
                "POSTGRES_PASSWORD": settings.POSTGRES_PASSWORD,
                "POSTGRES_HOST": settings.POSTGRES_HOST,
                "POSTGRES_PORT": str(settings.POSTGRES_PORT),
                "POSTGRES_DB": settings.POSTGRES_DB,
                "DATABASE_URL": settings.DATABASE_URL,
            }
        )

        subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            cwd=Path(__file__).parent,
            env=env,
        )
        logger.info("Database migrations completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running database migrations: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    logger.info("Starting application")
    # Test all logger namespaces
    domain_logger.debug("Testing domain debug log")
    domain_logger.info("Testing domain info log")
    app_logger.debug("Testing application debug log")
    app_logger.info("Testing application info log")
    infra_logger.debug("Testing infrastructure debug log")
    infra_logger.info("Testing infrastructure info log")
    interface_logger.debug("Testing interface debug log")
    interface_logger.info("Testing interface info log")

    # Run database migrations
    run_migrations()
    # Start the server
    logger.info("Initializing web server")
    start_server(reload=True)  # Enable reload for development

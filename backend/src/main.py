import subprocess
import sys
from pathlib import Path
from infrastructure.web import start_server
from infrastructure.logging_config import setup_logging, get_logger

# Initialize logging
setup_logging()
logger = get_logger(__name__)

def run_migrations():
    """
    Run database migrations using Alembic.
    """
    alembic_ini_path = Path(__file__).parent / "alembic.ini"
    try:
        logger.info("Starting database migrations")
        subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            cwd=Path(__file__).parent
        )
        logger.info("Database migrations completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running database migrations: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    logger.info("Starting application")
    # Run database migrations
    run_migrations()
    # Start the server
    logger.info("Initializing web server")
    start_server(reload=True)  # Enable reload for development 
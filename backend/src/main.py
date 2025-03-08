import subprocess
import sys
from pathlib import Path
from infrastructure.web import start_server

def run_migrations():
    """
    Run database migrations using Alembic.
    """
    alembic_ini_path = Path(__file__).parent / "alembic.ini"
    try:
        subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            cwd=Path(__file__).parent
        )
        print("Database migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running database migrations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Run database migrations
    run_migrations()
    # Start the server
    start_server(reload=True)  # Enable reload for development 
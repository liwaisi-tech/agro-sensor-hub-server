from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Agro Sensor Hub"
    APP_VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    
    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "agro_sensor_hub"
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # API Settings
    API_PREFIX: str = "/agro-sensor-hub/api"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Allow missing .env file
        env_ignore_missing = True
        # Search for .env in parent directories
        env_file = [
            Path(".env"),
            Path("../.env"),
            Path("../../.env"),
        ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the settings.
    This ensures we don't load the environment variables multiple times.
    """
    return Settings()
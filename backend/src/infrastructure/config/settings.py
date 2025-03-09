from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Agro Sensor Hub"
    APP_VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    PORT: int = 8080
    
    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "0.0.0.0"  # Default for local development
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "agro_sensor_hub"
    DATABASE_URL: str = ""  # Will be set in __init__
    
    # API Settings
    API_PREFIX: str = "/agro-sensor-hub/api"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Allow missing .env file
        env_ignore_missing = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set DATABASE_URL after all variables are loaded
        self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the settings.
    This ensures we don't load the environment variables multiple times.
    """
    return Settings()
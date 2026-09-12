"""
Central application configuration.

Loads everything from environment variables (via a .env file).
Never hardcode secrets/keys here — this file only defines WHAT
settings exist and their defaults, not the actual values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Bazaar PSX Terminal"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/bazaar"
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://postgres:password@localhost:5432/bazaar"

    # Generic PSX data provider (placeholder until team confirms a real one)
    PSX_API_KEY: str = ""
    PSX_API_URL: str = "https://api.psx.com/v1"
    PSX_API_SECRET: str = ""

    # PyPSX SDK (alternative provider, not used by default)
    PYPSX_API_KEY_ID: str = ""
    PYPSX_API_SECRET_KEY: str = ""
    PYPSX_PAPER: bool = True
    USE_PYPSX: bool = False

    # JWT
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = '["http://localhost:3000"]'
    RATE_LIMIT_PER_MINUTE: int = 60

    # Optional cache
    REDIS_URL: str = "redis://localhost:6379"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        try:
            return json.loads(self.CORS_ORIGINS)
        except (json.JSONDecodeError, TypeError):
            return ["http://localhost:3000"]


# Single shared instance — import this everywhere else
settings = Settings()

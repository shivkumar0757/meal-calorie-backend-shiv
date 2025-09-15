"""
Profile-based configuration for FastAPI application
Supports: dev (SQLite), local (PostgreSQL), prod (PostgreSQL)
"""

import os
from enum import Enum
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Environment(str, Enum):
    """Supported environment profiles"""

    DEV = "dev"
    LOCAL = "local"
    PROD = "prod"


class Settings(BaseSettings):
    """Application settings with profile-based configuration"""

    # Environment Profile
    environment: Environment = Field(default=Environment.DEV, env="ENVIRONMENT")

    # Database Configuration (profile-dependent)
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")

    # USDA API Configuration
    usda_api_key: str = Field(..., env="USDA_API_KEY")

    # JWT Configuration
    jwt_secret: str = Field(default="dev-secret-change-in-production", env="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(
        default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # API Configuration
    api_rate_limit: int = Field(default=100, env="API_RATE_LIMIT")

    # Cache Configuration
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")

    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")

    class Config:
        # Pydantic automatically loads the profile-specific env file
        profile_env = f".env.{os.getenv('ENVIRONMENT', 'dev')}"
        env_file = [".env", profile_env] if os.path.exists(profile_env) else ".env"
        case_sensitive = False

    @property
    def effective_database_url(self) -> str:
        """Get database URL based on environment profile"""

        # If DATABASE_URL is explicitly set, use it
        if self.database_url:
            # Profile-based database URL logic
            if self.environment == Environment.DEV:
                # Force SQLite for dev environment
                if not self.database_url.startswith("sqlite"):
                    logger.info("DEV profile: Forcing SQLite database")
                    return "sqlite:///./app_dev.db"
                return self.database_url

            elif self.environment in [Environment.LOCAL, Environment.PROD]:
                # Use PostgreSQL for local/prod
                if self.database_url.startswith("sqlite"):
                    # Override SQLite with default PostgreSQL for local/prod
                    logger.info(f"{self.environment.upper()} profile: Using PostgreSQL")
                    return (
                        "postgresql://meal_user:dev_password@localhost:5432/mealcalorie"
                    )
                return self.database_url

        # Default database URLs by profile
        default_urls = {
            Environment.DEV: "sqlite:///./app_dev.db",
            Environment.LOCAL: "postgresql://meal_user:dev_password@localhost:5432/mealcalorie",
            Environment.PROD: "postgresql://meal_user:prod_password@localhost:5432/mealcalorie_prod",
        }

        url = default_urls[self.environment]
        logger.info(
            f"Using {self.environment.upper()} profile database: {url.split('@')[0]}@***"
        )
        return url

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == Environment.DEV

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == Environment.PROD


# Global settings instance
settings = Settings()

# Log current configuration
logger.info(f"Environment Profile: {settings.environment.upper()}")
logger.info(
    f"Database: {'SQLite' if settings.effective_database_url.startswith('sqlite') else 'PostgreSQL'}"
)
logger.info(f"Server: {settings.host}:{settings.port}")
logger.info(f"Rate Limit: {settings.api_rate_limit}/min")

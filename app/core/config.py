import os
from functools import lru_cache
from urllib.parse import quote_plus, urlparse

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Team Task Manager"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field(default="change-me-1234567890abcdefghijklmnop", alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    mysql_user: str = Field(default="root", alias="MYSQL_USER")
    mysql_password: str = Field(default="", alias="MYSQL_PASSWORD")
    mysql_host: str = Field(default="127.0.0.1", alias="MYSQL_HOST")
    mysql_port: int = Field(default=3306, alias="MYSQL_PORT")
    mysql_database: str = Field(default="team_task_manager", alias="MYSQL_DATABASE")
    admin_name: str | None = Field(default=None, validation_alias=AliasChoices("ADMIN_NAME", "ADMIN_USERNAME"))
    admin_email: str | None = Field(default=None, alias="ADMIN_EMAIL")
    admin_password: str | None = Field(default=None, alias="ADMIN_PASSWORD")
    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")
    create_tables_on_startup: bool = Field(default=True, alias="CREATE_TABLES_ON_STARTUP")

    @property
    def is_railway_environment(self) -> bool:
        """Detect if running on Railway platform"""
        return bool(os.getenv("RAILWAY_ENVIRONMENT")) or bool(os.getenv("RAILWAY_PRIVATE_DOMAIN"))

    @property
    def sqlalchemy_database_url(self) -> str:
        """Get database URL with Railway-aware configuration"""
        # Railway environment: DATABASE_URL is REQUIRED
        if self.is_railway_environment:
            if not self.database_url:
                raise ValueError(
                    "DATABASE_URL environment variable is required on Railway. "
                    "Ensure MySQL service is added and the environment variable is set."
                )
            return self.database_url
        
        # Local development: Use DATABASE_URL if provided, otherwise construct from components
        if self.database_url:
            return self.database_url
        
        # Construct from individual variables (local development only)
        password = quote_plus(self.mysql_password)
        return (
            f"mysql+pymysql://{self.mysql_user}:{password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    def get_db_host(self) -> str:
        """Extract and return the database host for logging"""
        try:
            parsed = urlparse(self.sqlalchemy_database_url)
            return parsed.hostname or "unknown"
        except Exception:
            return "unknown"

    @property
    def cors_origin_list(self) -> list[str]:
        # Allow all origins by default (safer for development/Railway)
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

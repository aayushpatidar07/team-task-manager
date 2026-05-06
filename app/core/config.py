import os
from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Team Task Manager"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
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
    cors_origins: str = Field(default="http://localhost:8000,http://127.0.0.1:8000", alias="CORS_ORIGINS")
    create_tables_on_startup: bool = Field(default=True, alias="CREATE_TABLES_ON_STARTUP")

    @property
    def sqlalchemy_database_url(self) -> str:
        # Prefer environment DATABASE_URL (Railway, managed services)
        if self.database_url:
            return self.database_url
        
        # Fallback: construct from individual variables (local development)
        password = quote_plus(self.mysql_password)
        return (
            f"mysql+pymysql://{self.mysql_user}:{password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    def is_production(self) -> bool:
        """Check if running in production environment (Railway)"""
        return bool(self.database_url and ("railway.app" in self.database_url or ":" in self.database_url))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

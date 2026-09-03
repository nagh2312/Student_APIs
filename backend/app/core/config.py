"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Student API Platform"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False
    mock_mode: bool = True

    api_base_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000"

    database_url: str = (
        "postgresql+asyncpg://studentapi:studentapi@localhost:5432/studentapi"
    )
    redis_url: str = "redis://localhost:6379/0"

    rate_limit_anonymous: int = 60
    rate_limit_authenticated: int = 300
    rate_limit_window_seconds: int = 60

    cache_ttl_weather: int = 600
    cache_ttl_currency: int = 3600
    cache_ttl_geography: int = 86400
    cache_ttl_books: int = 3600

    weather_provider: str = "openmeteo"
    weather_api_key: str = ""
    geography_provider: str = "nominatim"
    books_provider: str = "openlibrary"
    currency_provider: str = "frankfurter"

    api_key_pepper: str = "change-me-in-production"
    secret_key: str = "change-me-in-production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

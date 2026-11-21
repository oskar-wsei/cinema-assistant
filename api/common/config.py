from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..cinemacity.default import (
    DEFAULT_BASE_URL,
    DEFAULT_TENANT_ID,
    DEFAULT_TIMEOUT_SECONDS,
)


class Settings(BaseSettings):
    """Application settings, read from ``CINEMACITY_*`` environment variables."""

    model_config = SettingsConfigDict(env_prefix='CINEMACITY_', env_file='.env')

    base_url: str = DEFAULT_BASE_URL
    tenant_id: str = DEFAULT_TENANT_ID
    language: str | None = Field(
        default=None, description='Response locale, e.g. "pl_PL" or "en_GB".'
    )
    timeout_seconds: float = Field(default=DEFAULT_TIMEOUT_SECONDS, gt=0)
    cache_ttl_seconds: int = Field(
        default=300, ge=0, description='Upstream response cache TTL; 0 disables it.'
    )
    cors_origins: list[str] = Field(default=['*'])


@lru_cache
def get_settings() -> Settings:
    return Settings()

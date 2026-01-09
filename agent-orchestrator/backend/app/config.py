"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # === Application ===
    app_name: str = "Agent Orchestrator"
    debug: bool = False

    # === Database ===
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/orchestrator"

    # === Redis ===
    redis_url: str = "redis://localhost:6379"

    # === LLM - Planning Tier ===
    anthropic_api_key: str = ""

    # === LLM - Execution Tier ===
    execution_llm_url: str = "http://localhost:11434"
    execution_llm_model: str = "qwen2.5-coder:32b"
    openrouter_api_key: str = ""

    # === Security ===
    api_key: str = Field(
        ...,
        min_length=32,
        description="API key for authentication (min 32 characters)",
    )

    # === CORS ===
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="List of allowed CORS origins",
    )

    # === Cost Management ===
    daily_budget_usd: float = 5.0

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate API key length and format."""
        if len(v) < 32:
            raise ValueError("API key must be at least 32 characters long")
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

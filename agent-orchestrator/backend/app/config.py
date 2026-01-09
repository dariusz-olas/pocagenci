"""Application configuration using Pydantic Settings."""

from functools import lru_cache
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
    api_key: str = "dev-api-key-change-in-production"

    # === Cost Management ===
    daily_budget_usd: float = 5.0


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

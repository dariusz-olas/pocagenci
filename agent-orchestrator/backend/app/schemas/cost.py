"""Pydantic schemas for Cost tracking."""

from pydantic import BaseModel, Field


class CostSummary(BaseModel):
    """Daily cost summary."""
    today_cloud_usd: float = Field(ge=0)
    today_tokens_input: int = Field(ge=0)
    today_tokens_output: int = Field(ge=0)
    budget_limit_usd: float = Field(ge=0)
    budget_remaining_usd: float
    budget_percent_used: float = Field(ge=0, le=100)


class CostEntry(BaseModel):
    """Single cost log entry."""
    tier: str  # "planning" or "execution"
    provider: str  # "anthropic", "openai", "ollama"
    input_tokens: int
    output_tokens: int
    cost_usd: float


class BudgetExceededError(BaseModel):
    """Error response when budget is exceeded."""
    error: str = "BUDGET_EXCEEDED"
    message: str = "Daily cloud LLM budget exceeded"
    details: dict  # {"current": 5.12, "limit": 5.00}

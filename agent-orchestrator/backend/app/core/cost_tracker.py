"""Cost tracking for LLM usage."""

from datetime import date
from typing import Optional
from redis.asyncio import Redis

from app.llm.router import LLMTier
from app.schemas.cost import CostSummary

# Pricing per 1M tokens (USD)
PRICING = {
    "anthropic": {"input": 3.00, "output": 15.00},  # Claude 3.5 Sonnet
    "openai": {"input": 2.50, "output": 10.00},     # GPT-4o
    "ollama": {"input": 0.0, "output": 0.0},        # Local - free
}


class CostTracker:
    """Tracks LLM usage costs with Redis backend."""

    def __init__(self, redis: Optional[Redis] = None, daily_budget: float = 5.0):
        self.redis = redis
        self.daily_budget = daily_budget

    async def log(
        self,
        tier: LLMTier,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: Optional[float] = None,
    ) -> None:
        """Log LLM usage and cost.

        Args:
            tier: LLM tier (planning/execution)
            provider: Provider name (anthropic, openai, ollama)
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost_usd: Override cost (for execution tier = 0)
        """
        if cost_usd is None and tier == LLMTier.PLANNING:
            pricing = PRICING.get(provider, PRICING["anthropic"])
            cost_usd = (
                (input_tokens / 1_000_000) * pricing["input"] +
                (output_tokens / 1_000_000) * pricing["output"]
            )
        elif cost_usd is None:
            cost_usd = 0.0

        today = date.today().isoformat()

        if self.redis:
            pipe = self.redis.pipeline()
            pipe.incrbyfloat(f"cost:{today}:cloud", cost_usd)
            pipe.incrby(f"tokens:{today}:input", input_tokens)
            pipe.incrby(f"tokens:{today}:output", output_tokens)
            pipe.expire(f"cost:{today}:cloud", 86400 * 7)  # 7 days TTL
            pipe.expire(f"tokens:{today}:input", 86400 * 7)
            pipe.expire(f"tokens:{today}:output", 86400 * 7)
            await pipe.execute()

    async def get_summary(self) -> CostSummary:
        """Get today's cost summary.

        Returns:
            CostSummary with current usage and budget status
        """
        today = date.today().isoformat()

        if self.redis:
            cloud_cost = float(await self.redis.get(f"cost:{today}:cloud") or 0)
            input_tokens = int(await self.redis.get(f"tokens:{today}:input") or 0)
            output_tokens = int(await self.redis.get(f"tokens:{today}:output") or 0)
        else:
            cloud_cost = 0.0
            input_tokens = 0
            output_tokens = 0

        remaining = self.daily_budget - cloud_cost
        percent_used = (cloud_cost / self.daily_budget * 100) if self.daily_budget > 0 else 0

        return CostSummary(
            today_cloud_usd=round(cloud_cost, 4),
            today_tokens_input=input_tokens,
            today_tokens_output=output_tokens,
            budget_limit_usd=self.daily_budget,
            budget_remaining_usd=round(remaining, 4),
            budget_percent_used=round(percent_used, 2),
        )

    async def is_budget_exceeded(self) -> bool:
        """Check if daily budget is exceeded.

        Returns:
            True if budget exceeded
        """
        summary = await self.get_summary()
        return summary.today_cloud_usd >= self.daily_budget

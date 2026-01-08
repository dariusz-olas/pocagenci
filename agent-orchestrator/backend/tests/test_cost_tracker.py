"""Tests for CostTracker."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.cost_tracker import CostTracker, PRICING
from app.llm.router import LLMTier


@pytest.fixture
def mock_redis():
    """Create mock Redis client."""
    redis = MagicMock()
    redis.get = AsyncMock(return_value=None)
    redis.pipeline = MagicMock()

    pipe = MagicMock()
    pipe.incrbyfloat = MagicMock(return_value=pipe)
    pipe.incrby = MagicMock(return_value=pipe)
    pipe.expire = MagicMock(return_value=pipe)
    pipe.execute = AsyncMock(return_value=[])

    redis.pipeline.return_value = pipe
    return redis


@pytest.fixture
def cost_tracker(mock_redis):
    """Create CostTracker with mock Redis."""
    return CostTracker(redis=mock_redis, daily_budget=5.0)


@pytest.mark.asyncio
async def test_get_summary_empty(cost_tracker):
    """Test get_summary with no usage."""
    summary = await cost_tracker.get_summary()

    assert summary.today_cloud_usd == 0.0
    assert summary.budget_remaining_usd == 5.0
    assert summary.budget_percent_used == 0.0


@pytest.mark.asyncio
async def test_is_budget_exceeded_false(cost_tracker):
    """Test budget not exceeded when under limit."""
    exceeded = await cost_tracker.is_budget_exceeded()
    assert exceeded is False


@pytest.mark.asyncio
async def test_is_budget_exceeded_true(cost_tracker, mock_redis):
    """Test budget exceeded when over limit."""
    mock_redis.get = AsyncMock(return_value="5.50")  # Over $5 budget

    exceeded = await cost_tracker.is_budget_exceeded()
    assert exceeded is True


@pytest.mark.asyncio
async def test_log_planning_tier(cost_tracker, mock_redis):
    """Test logging planning tier usage."""
    await cost_tracker.log(
        tier=LLMTier.PLANNING,
        provider="anthropic",
        input_tokens=1000,
        output_tokens=500,
    )

    # Verify pipeline was called
    mock_redis.pipeline.assert_called_once()


def test_pricing_constants():
    """Test pricing constants are set."""
    assert "anthropic" in PRICING
    assert PRICING["anthropic"]["input"] > 0
    assert PRICING["anthropic"]["output"] > 0
    assert PRICING["ollama"]["input"] == 0
    assert PRICING["ollama"]["output"] == 0

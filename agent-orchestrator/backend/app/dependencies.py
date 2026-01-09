"""FastAPI dependencies for dependency injection."""

from typing import AsyncGenerator
from fastapi import Depends, HTTPException, Header, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import Settings, get_settings
from app.llm import LLMRouter, AnthropicProvider, OpenAICompatibleProvider
from app.core import CostTracker, TaskDecomposer, ExecutionEngine
from app.adapters import CrewAIAdapter

# Global instances (initialized on startup)
_engine = None
_session_factory = None
_redis: Redis | None = None
_llm_router: LLMRouter | None = None
_cost_tracker: CostTracker | None = None
_crewai_adapter: CrewAIAdapter | None = None
_execution_engine: ExecutionEngine | None = None


async def init_dependencies(settings: Settings):
    """Initialize all dependencies (called on app startup)."""
    global _engine, _session_factory, _redis, _llm_router, _cost_tracker, _crewai_adapter, _execution_engine

    # Database
    _engine = create_async_engine(settings.database_url, echo=settings.debug)
    _session_factory = async_sessionmaker(_engine, expire_on_commit=False)

    # Redis
    _redis = Redis.from_url(settings.redis_url)

    # Cost Tracker
    _cost_tracker = CostTracker(redis=_redis, daily_budget=settings.daily_budget_usd)

    # LLM Providers
    planning_provider = AnthropicProvider(api_key=settings.anthropic_api_key)
    
    # Build execution LLM URL - handle both with and without /v1 suffix
    execution_url = settings.execution_llm_url.rstrip("/")
    if not execution_url.endswith("/v1"):
        execution_url = f"{execution_url}/v1"
    
    execution_provider = OpenAICompatibleProvider(
        base_url=execution_url,
        model=settings.execution_llm_model,
    )

    # LLM Router
    _llm_router = LLMRouter(
        planning_provider=planning_provider,
        execution_provider=execution_provider,
        cost_tracker=_cost_tracker,
    )

    # CrewAI Adapter
    _crewai_adapter = CrewAIAdapter(llm_router=_llm_router)

    # Execution Engine
    _execution_engine = ExecutionEngine(adapter=_crewai_adapter)


async def cleanup_dependencies():
    """Cleanup dependencies (called on app shutdown)."""
    global _engine, _redis
    if _redis:
        await _redis.close()
    if _engine:
        await _engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    if _session_factory is None:
        raise RuntimeError("Database not initialized")
    async with _session_factory() as session:
        yield session


def get_redis() -> Redis:
    """Get Redis client."""
    if _redis is None:
        raise RuntimeError("Redis not initialized")
    return _redis


def get_llm_router() -> LLMRouter:
    """Get LLM router."""
    if _llm_router is None:
        raise RuntimeError("LLM Router not initialized")
    return _llm_router


def get_cost_tracker() -> CostTracker:
    """Get cost tracker."""
    if _cost_tracker is None:
        raise RuntimeError("Cost tracker not initialized")
    return _cost_tracker


def get_task_decomposer(
    llm_router: LLMRouter = Depends(get_llm_router),
) -> TaskDecomposer:
    """Get task decomposer."""
    return TaskDecomposer(llm_router)


def get_execution_engine() -> ExecutionEngine:
    """Get execution engine."""
    if _execution_engine is None:
        raise RuntimeError("Execution engine not initialized")
    return _execution_engine


def get_crewai_adapter() -> CrewAIAdapter:
    """Get CrewAI adapter."""
    if _crewai_adapter is None:
        raise RuntimeError("CrewAI adapter not initialized")
    return _crewai_adapter


async def verify_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    settings: Settings = Depends(get_settings),
) -> str:
    """Verify API key from header."""
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return x_api_key


# Rate limiting dependencies
from app.middleware import create_rate_limit_dependency

# General rate limit: 100 requests per minute
verify_api_key_with_rate_limit = create_rate_limit_dependency(
    redis_getter=get_redis,
    max_requests=100,
    window_seconds=60,
    endpoint_name="general",
)

# Decompose endpoint rate limit: 10 requests per minute
verify_api_key_decompose = create_rate_limit_dependency(
    redis_getter=get_redis,
    max_requests=10,
    window_seconds=60,
    endpoint_name="decompose",
)

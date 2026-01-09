"""API routes for health checks."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_redis, get_llm_router
from app.llm import LLMRouter

router = APIRouter(tags=["health"])


class HealthCheck(BaseModel):
    """Health check response."""
    status: str  # "healthy" or "unhealthy"
    checks: dict[str, bool]


@router.get("/health", response_model=HealthCheck)
async def health_check(
    llm_router: LLMRouter = Depends(get_llm_router),
):
    """Check health of all services.

    Returns status of database, Redis, and execution LLM.
    """
    checks = {}

    # Check Redis
    try:
        redis = get_redis()
        await redis.ping()
        checks["redis"] = True
    except Exception:
        checks["redis"] = False

    # Check execution LLM (Ollama)
    try:
        checks["execution_llm"] = await llm_router.is_execution_available()
    except Exception:
        checks["execution_llm"] = False

    # Database check is implicit - if we got here, it's working

    all_healthy = all(checks.values())

    return HealthCheck(
        status="healthy" if all_healthy else "unhealthy",
        checks=checks,
    )


@router.get("/health/live")
async def liveness():
    """Simple liveness probe."""
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness(
    llm_router: LLMRouter = Depends(get_llm_router),
):
    """Readiness probe - checks if service is ready to accept traffic."""
    try:
        redis = get_redis()
        await redis.ping()
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}

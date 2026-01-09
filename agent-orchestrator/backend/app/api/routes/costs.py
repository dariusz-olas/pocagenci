"""API routes for cost tracking."""

from fastapi import APIRouter, Depends

from app.dependencies import get_cost_tracker, verify_api_key
from app.schemas import CostSummary
from app.core import CostTracker

router = APIRouter(prefix="/costs", tags=["costs"])


@router.get("/summary", response_model=CostSummary)
async def get_cost_summary(
    cost_tracker: CostTracker = Depends(get_cost_tracker),
    _: str = Depends(verify_api_key),
):
    """Get today's cost summary.

    Returns current cloud LLM usage, token counts, and budget status.
    """
    return await cost_tracker.get_summary()

"""API routes for execution management."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db, verify_api_key
from app.schemas import ExecutionResponse, ExecutionLogEntry
from app.models import Execution

router = APIRouter(prefix="/executions", tags=["executions"])


@router.get("/{execution_id}", response_model=ExecutionResponse)
async def get_execution(
    execution_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Get execution by ID with logs and status.

    This endpoint returns the current state of an execution,
    including logs, status, output, and timing information.
    """
    result = await db.execute(select(Execution).where(Execution.id == execution_id))
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Execution {execution_id} not found",
        )

    # Parse logs from JSON to ExecutionLogEntry objects
    log_entries = []
    if execution.logs:
        for log in execution.logs:
            if isinstance(log, dict):
                log_entries.append(
                    ExecutionLogEntry(
                        timestamp=log.get("timestamp"),
                        level=log.get("level", "info"),
                        message=log.get("message", ""),
                        agent=log.get("agent"),
                    )
                )

    return ExecutionResponse(
        id=str(execution.id),
        task_id=str(execution.task_id),
        status=execution.status,
        output=execution.output,
        logs=log_entries,
        started_at=execution.started_at,
        completed_at=execution.completed_at,
        execution_time_seconds=execution.execution_time_seconds,
    )

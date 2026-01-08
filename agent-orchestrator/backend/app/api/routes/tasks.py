"""API routes for task management."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db, get_task_decomposer, get_cost_tracker, verify_api_key
from app.schemas import (
    TaskCreateRequest,
    TaskDecomposeRequest,
    TaskResponse,
    TaskDecomposition,
    TaskStatus,
    ExecutionCreateResponse,
    ExecutionStatus,
)
from app.models import Task, SubTask, Execution
from app.core import TaskDecomposer, CostTracker

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/decompose", response_model=TaskDecomposition)
async def decompose_task(
    request: TaskDecomposeRequest,
    decomposer: TaskDecomposer = Depends(get_task_decomposer),
    cost_tracker: CostTracker = Depends(get_cost_tracker),
    _: str = Depends(verify_api_key),
):
    """Decompose a task into subtasks using planning LLM.

    This endpoint uses the cloud LLM (planning tier) to analyze
    the task and break it down into executable subtasks.
    """
    # Check budget
    if await cost_tracker.is_budget_exceeded():
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "error": "BUDGET_EXCEEDED",
                "message": "Daily cloud LLM budget exceeded",
            },
        )

    try:
        decomposition = await decomposer.decompose(request.description)
        return decomposition
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decomposition failed: {str(e)}",
        )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Create a new task."""
    task = Task(description=request.description, status=TaskStatus.PENDING)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    return TaskResponse(
        id=str(task.id),
        description=task.description,
        status=task.status,
        subtasks=[],
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Get task by ID with subtasks."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    return TaskResponse(
        id=str(task.id),
        description=task.description,
        status=task.status,
        subtasks=[],  # TODO: Load subtasks
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.post("/{task_id}/execute", response_model=ExecutionCreateResponse)
async def execute_task(
    task_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Start task execution.

    Creates an execution record and starts the execution in the background.
    Use WebSocket endpoint to monitor progress.
    """
    # Get task
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    if task.status not in [TaskStatus.READY, TaskStatus.PENDING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task is in {task.status} state, cannot execute",
        )

    # Create execution
    execution = Execution(
        task_id=task.id,
        status=ExecutionStatus.QUEUED,
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)

    # TODO: Add background task to run execution
    # background_tasks.add_task(run_execution, execution.id)

    return ExecutionCreateResponse(
        execution_id=str(execution.id),
        task_id=str(task.id),
        status=ExecutionStatus.QUEUED,
    )

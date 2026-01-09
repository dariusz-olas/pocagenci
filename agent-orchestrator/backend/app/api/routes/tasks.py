"""API routes for task management."""

from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dependencies import (
    get_db,
    get_task_decomposer,
    get_cost_tracker,
    get_execution_engine,
    verify_api_key,
    verify_api_key_decompose,
)
from app.schemas import (
    TaskCreateRequest,
    TaskDecomposeRequest,
    TaskResponse,
    SubTaskResponse,
    TaskDecomposition,
    TaskStatus,
    ExecutionCreateResponse,
    ExecutionStatus,
)
from app.models import Task, SubTask, Execution
from app.core import TaskDecomposer, CostTracker, ExecutionEngine

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/decompose", response_model=TaskDecomposition)
async def decompose_task(
    request: TaskDecomposeRequest,
    decomposer: TaskDecomposer = Depends(get_task_decomposer),
    cost_tracker: CostTracker = Depends(get_cost_tracker),
    _: str = Depends(verify_api_key_decompose),
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
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id)
        .options(selectinload(Task.subtasks))
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    # Map subtasks to response schema
    subtasks_response = [
        SubTaskResponse(
            id=str(st.id),
            title=st.title,
            description=st.description,
            complexity=st.complexity,
            dependencies=st.dependencies,
            acceptance_criteria=st.acceptance_criteria,
            status=st.status,
        )
        for st in task.subtasks
    ]

    return TaskResponse(
        id=str(task.id),
        description=task.description,
        status=task.status,
        subtasks=subtasks_response,
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

    # Start background execution
    background_tasks.add_task(run_execution, execution.id)

    return ExecutionCreateResponse(
        execution_id=str(execution.id),
        task_id=str(task.id),
        status=ExecutionStatus.QUEUED,
    )


async def run_execution(execution_id: UUID):
    """Run task execution in background.

    This function is called by FastAPI's BackgroundTasks.
    It executes the task using the ExecutionEngine and updates
    the execution record with results.
    """
    from app.dependencies import get_db, get_crewai_adapter
    from app.api.websockets.progress import send_progress_update

    # Create a new ExecutionEngine instance for this execution
    # to avoid callback accumulation in global instance
    adapter = get_crewai_adapter()
    engine = ExecutionEngine(adapter=adapter)

    # Register WebSocket callback for progress updates
    engine.on_progress(send_progress_update)

    # Create a new database session for background task
    async for db in get_db():
        try:
            # Load execution and task with subtasks
            result = await db.execute(
                select(Execution)
                .where(Execution.id == execution_id)
                .options(selectinload(Execution.task).selectinload(Task.subtasks))
            )
            execution = result.scalar_one_or_none()

            if not execution:
                return

            task = execution.task

            # Update status to RUNNING
            execution.status = ExecutionStatus.RUNNING
            execution.started_at = datetime.utcnow()
            await db.commit()

            # Prepare subtasks data from task.decomposition_data or task.subtasks
            subtasks = []
            execution_order = []

            if task.decomposition_data:
                # Use decomposition data if available
                subtasks = task.decomposition_data.get("subtasks", [])
                execution_order = task.decomposition_data.get("execution_order", [])
            elif task.subtasks:
                # Fallback to subtasks from DB
                subtasks = [
                    {
                        "title": st.title,
                        "description": st.description,
                    }
                    for st in task.subtasks
                ]
                # Simple sequential execution order
                execution_order = [[st.title] for st in task.subtasks]

            if not subtasks:
                # No subtasks to execute
                execution.status = ExecutionStatus.FAILED
                execution.output = "No subtasks defined for execution"
                execution.completed_at = datetime.utcnow()
                execution.execution_time_seconds = (
                    execution.completed_at - execution.started_at
                ).total_seconds()
                await db.commit()
                return

            # Execute task through engine
            result = await engine.execute_task(
                execution_id=str(execution_id),
                subtasks=subtasks,
                execution_order=execution_order,
            )

            # Update execution with results
            execution.completed_at = datetime.utcnow()
            execution.execution_time_seconds = (
                execution.completed_at - execution.started_at
            ).total_seconds()

            if result.get("success"):
                execution.status = ExecutionStatus.COMPLETED
                execution.output = str(result.get("results", {}))
            else:
                execution.status = ExecutionStatus.FAILED
                execution.output = f"Execution failed: {result.get('results', {})}"

            # Update task status
            task.status = TaskStatus.COMPLETED if result.get("success") else TaskStatus.FAILED

            await db.commit()

        except Exception as e:
            # Handle any errors during execution
            try:
                execution.status = ExecutionStatus.FAILED
                execution.output = f"Error during execution: {str(e)}"
                execution.completed_at = datetime.utcnow()
                if execution.started_at:
                    execution.execution_time_seconds = (
                        execution.completed_at - execution.started_at
                    ).total_seconds()
                await db.commit()
            except Exception:
                pass  # Silently fail if we can't update the error state
        finally:
            break  # Exit the async generator

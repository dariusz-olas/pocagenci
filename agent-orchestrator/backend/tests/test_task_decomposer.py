"""Tests for TaskDecomposer."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.task_decomposer import TaskDecomposer
from app.schemas.task import TaskDecomposition, SubTaskBase, SubTaskComplexity


@pytest.fixture
def mock_llm_router():
    """Create mock LLM router."""
    router = MagicMock()
    router.planning_call = AsyncMock()
    return router


@pytest.fixture
def decomposer(mock_llm_router):
    """Create TaskDecomposer with mock router."""
    return TaskDecomposer(mock_llm_router)


@pytest.mark.asyncio
async def test_decompose_returns_task_decomposition(decomposer, mock_llm_router):
    """Test that decompose returns TaskDecomposition."""
    # Arrange
    expected = TaskDecomposition(
        original_task="Create a REST API",
        subtasks=[
            SubTaskBase(
                title="Setup FastAPI",
                description="Create main.py with FastAPI app",
                complexity=SubTaskComplexity.SIMPLE,
                dependencies=[],
                acceptance_criteria=["FastAPI app runs"],
            ),
        ],
        execution_order=[["Setup FastAPI"]],
        estimated_cost_usd=0.05,
    )
    mock_llm_router.planning_call.return_value = expected

    # Act
    result = await decomposer.decompose("Create a REST API")

    # Assert
    assert isinstance(result, TaskDecomposition)
    assert result.original_task == "Create a REST API"
    assert len(result.subtasks) == 1
    mock_llm_router.planning_call.assert_called_once()


@pytest.mark.asyncio
async def test_validate_decomposition_valid(decomposer):
    """Test validation passes for valid decomposition."""
    decomposition = TaskDecomposition(
        original_task="Test task",
        subtasks=[
            SubTaskBase(
                title="Step 1",
                description="Do step 1",
                complexity=SubTaskComplexity.SIMPLE,
                dependencies=[],
                acceptance_criteria=["Done"],
            ),
        ],
        execution_order=[["Step 1"]],
        estimated_cost_usd=0.01,
    )

    errors = await decomposer.validate_decomposition(decomposition)
    assert errors == []


@pytest.mark.asyncio
async def test_validate_decomposition_no_subtasks(decomposer):
    """Test validation fails when no subtasks."""
    decomposition = TaskDecomposition(
        original_task="Test",
        subtasks=[],
        execution_order=[],
        estimated_cost_usd=0.0,
    )

    errors = await decomposer.validate_decomposition(decomposition)
    assert "no subtasks" in errors[0].lower()

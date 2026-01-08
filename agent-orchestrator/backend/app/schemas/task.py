"""Pydantic schemas for Task domain."""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status of a task."""
    PENDING = "pending"
    DECOMPOSING = "decomposing"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class SubTaskComplexity(str, Enum):
    """Complexity level of a subtask."""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


# === Request Schemas ===

class TaskCreateRequest(BaseModel):
    """Request to create a new task."""
    description: str = Field(..., min_length=10, max_length=5000)


class TaskDecomposeRequest(BaseModel):
    """Request to decompose a task into subtasks."""
    description: str = Field(..., min_length=10, max_length=5000)


# === SubTask Schemas ===

class SubTaskBase(BaseModel):
    """Base schema for subtask."""
    title: str
    description: str
    complexity: SubTaskComplexity
    dependencies: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)


class SubTaskResponse(SubTaskBase):
    """Subtask in API response."""
    id: str
    status: TaskStatus = TaskStatus.PENDING


# === Task Schemas ===

class TaskDecomposition(BaseModel):
    """Result of task decomposition by LLM."""
    original_task: str
    subtasks: list[SubTaskBase]
    execution_order: list[list[str]]  # Groups of parallel subtask IDs
    estimated_cost_usd: float = Field(ge=0)


class TaskResponse(BaseModel):
    """Task in API response."""
    id: str
    description: str
    status: TaskStatus
    subtasks: list[SubTaskResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

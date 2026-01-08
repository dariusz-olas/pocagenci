"""Pydantic schemas for Execution domain."""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Status of an execution."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionCreateResponse(BaseModel):
    """Response after starting an execution."""
    execution_id: str
    task_id: str
    status: ExecutionStatus = ExecutionStatus.QUEUED


class ExecutionLogEntry(BaseModel):
    """Single log entry from execution."""
    timestamp: datetime
    level: str  # "info", "warning", "error"
    message: str
    agent: Optional[str] = None


class ExecutionResponse(BaseModel):
    """Execution details in API response."""
    id: str
    task_id: str
    status: ExecutionStatus
    output: Optional[str] = None
    logs: list[ExecutionLogEntry] = Field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time_seconds: Optional[float] = None

    model_config = {"from_attributes": True}


class ExecutionProgress(BaseModel):
    """Real-time progress update via WebSocket."""
    execution_id: str
    type: str  # "status", "log", "complete", "error"
    data: dict

"""SQLAlchemy models for Task domain."""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    JSON,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base
from app.schemas.task import TaskStatus, SubTaskComplexity


class Task(Base):
    """Task model - main task submitted by user."""

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False
    )
    decomposition_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, onupdate=datetime.utcnow, nullable=True
    )

    # Relationships
    subtasks: Mapped[list["SubTask"]] = relationship(
        "SubTask", back_populates="parent_task", cascade="all, delete-orphan"
    )
    executions: Mapped[list["Execution"]] = relationship(
        "Execution", back_populates="task", cascade="all, delete-orphan"
    )


class SubTask(Base):
    """SubTask model - decomposed part of a main task."""

    __tablename__ = "subtasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    complexity: Mapped[SubTaskComplexity] = mapped_column(
        SQLEnum(SubTaskComplexity), nullable=False
    )
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False
    )
    dependencies: Mapped[list] = mapped_column(JSON, default=list)
    acceptance_criteria: Mapped[list] = mapped_column(JSON, default=list)
    order_index: Mapped[int] = mapped_column(default=0)

    # Relationships
    parent_task: Mapped["Task"] = relationship("Task", back_populates="subtasks")

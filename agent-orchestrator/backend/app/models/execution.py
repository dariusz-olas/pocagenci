"""SQLAlchemy models for Execution domain."""

import uuid
from datetime import datetime
from sqlalchemy import Text, DateTime, ForeignKey, Float, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base
from app.schemas.execution import ExecutionStatus


class Execution(Base):
    """Execution model - represents a single run of a task."""

    __tablename__ = "executions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False
    )
    status: Mapped[ExecutionStatus] = mapped_column(
        SQLEnum(ExecutionStatus), default=ExecutionStatus.QUEUED, nullable=False
    )
    output: Mapped[str | None] = mapped_column(Text, nullable=True)
    logs: Mapped[list] = mapped_column(JSON, default=list)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    execution_time_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    adapter_name: Mapped[str] = mapped_column(default="crewai")
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="executions")

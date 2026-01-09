"""AI agent framework adapters package."""

from app.adapters.base import BaseAdapter, AgentConfig, TaskResult
from app.adapters.crewai_adapter import CrewAIAdapter

__all__ = [
    "BaseAdapter",
    "AgentConfig",
    "TaskResult",
    "CrewAIAdapter",
]

"""Base adapter interface for AI agent frameworks."""

from abc import ABC, abstractmethod
from typing import Optional, Any
from pydantic import BaseModel

from app.llm import LLMRouter


class AgentConfig(BaseModel):
    """Configuration for creating an agent."""
    role: str
    goal: str
    backstory: Optional[str] = None
    llm_tier: str = "execution"  # "planning" or "execution"


class TaskResult(BaseModel):
    """Result of task execution."""
    success: bool
    output: str
    logs: list[str] = []
    execution_time_seconds: float = 0.0


class BaseAdapter(ABC):
    """Abstract base class for AI agent framework adapters."""

    def __init__(self, llm_router: LLMRouter):
        """Initialize adapter with LLM router.

        Args:
            llm_router: Router for LLM calls
        """
        self.llm = llm_router

    @property
    @abstractmethod
    def name(self) -> str:
        """Return adapter name (e.g., 'crewai', 'langgraph')."""
        pass

    @abstractmethod
    async def create_agent(self, config: AgentConfig) -> Any:
        """Create an agent with the given configuration.

        Args:
            config: Agent configuration

        Returns:
            Framework-specific agent object
        """
        pass

    @abstractmethod
    async def execute_task(
        self,
        agent: Any,
        task_description: str,
        context: Optional[dict] = None,
    ) -> TaskResult:
        """Execute a task using the agent.

        Args:
            agent: Agent object created by create_agent()
            task_description: Description of the task
            context: Optional context from previous tasks

        Returns:
            TaskResult with success status and output
        """
        pass

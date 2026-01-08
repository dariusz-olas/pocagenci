"""LLM Router - routes requests to appropriate LLM tier."""

from enum import Enum
from typing import Optional, Type, TypeVar
from pydantic import BaseModel

from app.llm.providers.anthropic import AnthropicProvider
from app.llm.providers.openai_compatible import OpenAICompatibleProvider

T = TypeVar("T", bound=BaseModel)


class LLMTier(str, Enum):
    """LLM tier for cost tracking."""
    PLANNING = "planning"
    EXECUTION = "execution"


class LLMRouter:
    """Routes LLM calls to appropriate tier based on task type."""

    def __init__(
        self,
        planning_provider: AnthropicProvider,
        execution_provider: OpenAICompatibleProvider,
        cost_tracker=None,  # Injected later to avoid circular import
    ):
        self.planning = planning_provider
        self.execution = execution_provider
        self.cost_tracker = cost_tracker

    def set_cost_tracker(self, cost_tracker):
        """Set cost tracker (called after initialization)."""
        self.cost_tracker = cost_tracker

    async def planning_call(
        self,
        prompt: str,
        response_model: Optional[Type[T]] = None,
        max_tokens: int = 2000,
    ) -> T | str:
        """Call planning tier LLM (Claude) - use sparingly!

        Args:
            prompt: User prompt
            response_model: Optional Pydantic model for structured output
            max_tokens: Maximum tokens in response

        Returns:
            Response from planning LLM
        """
        input_tokens = await self.planning.count_tokens(prompt)

        response = await self.planning.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            response_model=response_model,
        )

        output_tokens = await self.planning.count_tokens(str(response))

        # Log cost
        if self.cost_tracker:
            await self.cost_tracker.log(
                tier=LLMTier.PLANNING,
                provider="anthropic",
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

        return response

    async def execution_call(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
    ) -> str:
        """Call execution tier LLM (Ollama/OpenRouter) - main workhorse.

        Args:
            prompt: User prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            Response from execution LLM
        """
        input_tokens = await self.execution.count_tokens(prompt)

        response = await self.execution.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        output_tokens = await self.execution.count_tokens(response)

        # Log for stats (execution is free/cheap)
        if self.cost_tracker:
            await self.cost_tracker.log(
                tier=LLMTier.EXECUTION,
                provider="ollama",
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=0.0,
            )

        return response

    async def is_execution_available(self) -> bool:
        """Check if execution LLM is available."""
        return await self.execution.is_available()

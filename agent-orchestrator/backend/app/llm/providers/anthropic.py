"""Anthropic LLM provider for planning tier."""

from typing import Optional, Type, TypeVar
import anthropic
from pydantic import BaseModel
import instructor

T = TypeVar("T", bound=BaseModel)


class AnthropicProvider:
    """Anthropic Claude provider for high-quality planning tasks."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model
        # Wrap with instructor for structured outputs
        self.instructor_client = instructor.from_anthropic(self.client)

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        response_model: Optional[Type[T]] = None,
        system: str = "You are an expert AI assistant for task planning and decomposition.",
    ) -> T | str:
        """Generate response from Claude.

        Args:
            prompt: User prompt
            max_tokens: Maximum tokens in response
            response_model: Optional Pydantic model for structured output
            system: System prompt

        Returns:
            Structured response if response_model provided, else raw string
        """
        if response_model:
            # Use instructor for structured output
            response = await self.instructor_client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
                response_model=response_model,
            )
            return response

        # Raw response
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    async def count_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        # Anthropic uses ~4 chars per token on average
        return len(text) // 4

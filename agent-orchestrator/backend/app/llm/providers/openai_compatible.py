"""OpenAI-compatible LLM provider for execution tier (Ollama, OpenRouter)."""

from typing import Optional
import httpx
from openai import AsyncOpenAI


class OpenAICompatibleProvider:
    """OpenAI-compatible provider for local/cheap execution LLMs."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",  # Ollama doesn't need real key
        model: str = "qwen2.5-coder:32b",
    ):
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            http_client=httpx.AsyncClient(timeout=120.0),
        )
        self.model = model
        self.base_url = base_url

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        system: str = "You are an expert programmer. Write clean, efficient code.",
    ) -> str:
        """Generate response from execution LLM.

        Args:
            prompt: User prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            system: System prompt

        Returns:
            Generated text response
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

    async def is_available(self) -> bool:
        """Check if the LLM service is available."""
        try:
            # Try to list models
            await self.client.models.list()
            return True
        except Exception:
            return False

    async def count_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        # Rough estimate: ~4 chars per token
        return len(text) // 4

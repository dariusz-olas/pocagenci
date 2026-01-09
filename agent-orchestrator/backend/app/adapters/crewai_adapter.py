"""CrewAI framework adapter."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Any
import time

from crewai import Agent, Task, Crew, Process
from langchain_core.language_models.base import BaseLanguageModel

from app.adapters.base import BaseAdapter, AgentConfig, TaskResult
from app.llm import LLMRouter


class CrewAIAdapter(BaseAdapter):
    """Adapter for CrewAI framework.

    CrewAI is synchronous, so we run it in a thread pool
    to avoid blocking the async event loop.
    """

    def __init__(self, llm_router: LLMRouter):
        super().__init__(llm_router)
        self._executor = ThreadPoolExecutor(max_workers=4)

    @property
    def name(self) -> str:
        return "crewai"

    def _create_sync_llm_wrapper(self, tier: str) -> BaseLanguageModel:
        """Create synchronous LLM wrapper for CrewAI.

        CrewAI uses LangChain's language model interface, so we need
        to wrap our async router in a sync wrapper.
        """
        router = self.llm

        class SyncRouterLLM(BaseLanguageModel):
            """Sync wrapper around async LLM router."""

            @property
            def _llm_type(self) -> str:
                return "router"

            def _generate(
                self,
                prompts: list[str],
                stop: Optional[list[str]] = None,
                run_manager = None,
                **kwargs
            ):
                """Generate response - required by BaseLanguageModel."""
                from langchain_core.outputs import LLMResult, Generation
                loop = asyncio.new_event_loop()
                try:
                    result = ""
                    if tier == "planning":
                        result = loop.run_until_complete(router.planning_call(prompts[0]))
                    else:
                        result = loop.run_until_complete(router.execution_call(prompts[0]))
                    
                    return LLMResult(generations=[[Generation(text=result)]])
                finally:
                    loop.close()

            @property
            def _identifying_params(self) -> dict:
                return {"tier": tier}

        return SyncRouterLLM()

    async def create_agent(self, config: AgentConfig | dict) -> Agent:
        """Create a CrewAI agent.

        Args:
            config: Agent configuration (AgentConfig or dict)

        Returns:
            CrewAI Agent object
        """
        if isinstance(config, dict):
            config = AgentConfig(**config)

        llm = self._create_sync_llm_wrapper(config.llm_tier)

        return Agent(
            role=config.role,
            goal=config.goal,
            backstory=config.backstory or f"Expert {config.role}",
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )

    async def execute_task(
        self,
        agent: Agent,
        task_description: str,
        context: Optional[dict] = None,
    ) -> TaskResult:
        """Execute a task using CrewAI.

        Runs the synchronous CrewAI code in a thread pool.

        Args:
            agent: CrewAI Agent
            task_description: What to do
            context: Optional context from previous tasks

        Returns:
            TaskResult with success status and output
        """
        start = time.time()

        # Build context string if provided
        context_str = ""
        if context:
            context_str = "\n\nContext from previous tasks:\n"
            for task_name, output in context.items():
                context_str += f"- {task_name}: {output[:500]}...\n"

        full_description = task_description + context_str

        task = Task(
            description=full_description,
            agent=agent,
            expected_output="Task completed with deliverables",
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        # Run sync CrewAI kickoff in thread pool
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self._executor,
                crew.kickoff,
            )

            return TaskResult(
                success=True,
                output=str(result),
                logs=[],
                execution_time_seconds=time.time() - start,
            )

        except Exception as e:
            return TaskResult(
                success=False,
                output=str(e),
                logs=[f"Error: {e}"],
                execution_time_seconds=time.time() - start,
            )

    def __del__(self):
        """Cleanup thread pool."""
        self._executor.shutdown(wait=False)

"""Execution engine for running tasks through adapters."""

import asyncio
from datetime import datetime
from typing import Optional, Callable, Awaitable
from uuid import UUID

from app.schemas.execution import ExecutionStatus, ExecutionProgress
from app.schemas.task import TaskStatus


class ExecutionEngine:
    """Orchestrates task execution through framework adapters."""

    def __init__(self, adapter):
        """Initialize with a framework adapter.

        Args:
            adapter: Framework adapter (e.g., CrewAIAdapter)
        """
        self.adapter = adapter
        self._progress_callbacks: list[Callable[[ExecutionProgress], Awaitable[None]]] = []

    def on_progress(self, callback: Callable[[ExecutionProgress], Awaitable[None]]):
        """Register a progress callback (for WebSocket updates).

        Args:
            callback: Async function to call with progress updates
        """
        self._progress_callbacks.append(callback)

    async def _emit_progress(self, execution_id: str, type: str, data: dict):
        """Emit progress update to all callbacks.

        Args:
            execution_id: ID of the execution
            type: Event type (status, log, complete, error)
            data: Event data
        """
        progress = ExecutionProgress(
            execution_id=execution_id,
            type=type,
            data=data,
        )
        for callback in self._progress_callbacks:
            try:
                await callback(progress)
            except Exception:
                pass  # Don't let callback errors break execution

    async def execute_subtask(
        self,
        execution_id: str,
        subtask_title: str,
        subtask_description: str,
        context: Optional[dict] = None,
    ) -> dict:
        """Execute a single subtask.

        Args:
            execution_id: ID of the parent execution
            subtask_title: Title of the subtask
            subtask_description: Description of what to do
            context: Optional context from previous subtasks

        Returns:
            Result dict with success, output, execution_time
        """
        await self._emit_progress(
            execution_id,
            "status",
            {"status": ExecutionStatus.RUNNING, "subtask": subtask_title},
        )

        start_time = datetime.utcnow()

        try:
            # Create agent for this subtask
            agent = await self.adapter.create_agent({
                "role": "Developer",
                "goal": subtask_description,
                "backstory": f"Expert developer working on: {subtask_title}",
            })

            # Execute through adapter
            result = await self.adapter.execute_task(
                agent=agent,
                task_description=subtask_description,
                context=context,
            )

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            await self._emit_progress(
                execution_id,
                "log",
                {
                    "subtask": subtask_title,
                    "message": f"Completed in {execution_time:.2f}s",
                    "level": "info",
                },
            )

            return {
                "success": result.success,
                "output": result.output,
                "execution_time": execution_time,
            }

        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()

            await self._emit_progress(
                execution_id,
                "error",
                {"subtask": subtask_title, "error": str(e)},
            )

            return {
                "success": False,
                "output": str(e),
                "execution_time": execution_time,
            }

    async def execute_task(
        self,
        execution_id: str,
        subtasks: list[dict],
        execution_order: list[list[str]],
    ) -> dict:
        """Execute all subtasks in order.

        Args:
            execution_id: ID of the execution
            subtasks: List of subtask dicts with title, description
            execution_order: Groups of subtask titles to execute

        Returns:
            Final result with all subtask results
        """
        await self._emit_progress(
            execution_id,
            "status",
            {"status": ExecutionStatus.RUNNING, "message": "Starting execution"},
        )

        results = {}
        context = {}
        subtask_map = {st["title"]: st for st in subtasks}

        for group in execution_order:
            # Execute subtasks in this group in parallel
            group_tasks = []
            for title in group:
                if title in subtask_map:
                    st = subtask_map[title]
                    group_tasks.append(
                        self.execute_subtask(
                            execution_id=execution_id,
                            subtask_title=st["title"],
                            subtask_description=st["description"],
                            context=context,
                        )
                    )

            # Wait for all in group to complete
            group_results = await asyncio.gather(*group_tasks, return_exceptions=True)

            # Update context and results
            for title, result in zip(group, group_results):
                if isinstance(result, Exception):
                    results[title] = {"success": False, "output": str(result)}
                else:
                    results[title] = result
                    if result.get("success"):
                        context[title] = result.get("output", "")

        # Determine overall success
        all_success = all(r.get("success", False) for r in results.values())

        await self._emit_progress(
            execution_id,
            "complete",
            {
                "status": ExecutionStatus.COMPLETED if all_success else ExecutionStatus.FAILED,
                "results": results,
            },
        )

        return {
            "success": all_success,
            "results": results,
        }

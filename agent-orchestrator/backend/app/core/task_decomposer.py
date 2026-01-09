"""Task decomposition using planning LLM."""

import uuid
from app.llm.router import LLMRouter
from app.schemas.task import TaskDecomposition, SubTaskBase


DECOMPOSE_PROMPT = '''
Rozłóż poniższe zadanie programistyczne na mniejsze, wykonalne subtaski.

ZASADY:
1. Każdy subtask powinien być wykonalny w maksymalnie 30 minut
2. Określ zależności między taskami (które muszą być ukończone przed innymi)
3. Oznacz complexity:
   - "simple": proste zadania, np. utworzenie pliku, dodanie importu
   - "medium": średnie, np. implementacja funkcji, napisanie testu
   - "complex": złożone, np. projektowanie architektury, integracja
4. Podaj jasne acceptance_criteria dla każdego subtaska
5. execution_order to lista list - subtaski w tej samej liście mogą być wykonane równolegle

ZADANIE DO ROZBICIA:
{task}

Odpowiedz TYLKO jako JSON zgodny ze schematem:
{
  "original_task": "opis oryginalnego zadania",
  "subtasks": [
    {
      "title": "krótki tytuł",
      "description": "szczegółowy opis co zrobić",
      "complexity": "simple|medium|complex",
      "dependencies": ["id subtaska od którego zależy"],
      "acceptance_criteria": ["kryterium 1", "kryterium 2"]
    }
  ],
  "execution_order": [["subtask-1"], ["subtask-2", "subtask-3"], ["subtask-4"]],
  "estimated_cost_usd": 0.05
}
'''


class TaskDecomposer:
    """Decomposes complex tasks into subtasks using planning LLM."""

    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router

    async def decompose(self, task_description: str) -> TaskDecomposition:
        """Decompose a task into subtasks.

        Args:
            task_description: Description of the task to decompose

        Returns:
            TaskDecomposition with subtasks and execution order
        """
        prompt = DECOMPOSE_PROMPT.format(task=task_description)

        result = await self.llm.planning_call(
            prompt=prompt,
            response_model=TaskDecomposition,
            max_tokens=3000,
        )

        # Assign UUIDs to subtasks if not present
        for i, subtask in enumerate(result.subtasks):
            if not hasattr(subtask, 'id') or not subtask.id:
                # SubTaskBase doesn't have id, we'll add it when saving to DB
                pass

        return result

    async def validate_decomposition(self, decomposition: TaskDecomposition) -> list[str]:
        """Validate decomposition for common issues.

        Args:
            decomposition: The decomposition to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        if not decomposition.subtasks:
            errors.append("Decomposition has no subtasks")

        if not decomposition.execution_order:
            errors.append("Decomposition has no execution order")

        # Check all subtasks are in execution order
        subtask_titles = {st.title for st in decomposition.subtasks}
        order_titles = set()
        for group in decomposition.execution_order:
            order_titles.update(group)

        missing = subtask_titles - order_titles
        if missing:
            errors.append(f"Subtasks not in execution order: {missing}")

        return errors

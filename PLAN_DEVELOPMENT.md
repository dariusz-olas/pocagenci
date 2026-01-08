# Agent Orchestrator - Plan Developmentu POC

## 1. Wizja Projektu

**AgentOrchestrator** - meta-framework łączący funkcje z LangGraph, CrewAI, AutoGen i Agency Swarm, z hybrydową architekturą LLM (cloud do planowania + self-hosted do wykonania).

---

## 2. Architektura Hybrydowa LLM

```
PLANNING TIER (Cloud API - płatny, <5% wywołań)
├── Claude / GPT-4 / DeepSeek-V3
├── Zastosowanie: rozbijanie tasków, architektura, code review
└── Cel: minimalne koszty, maksymalna jakość decyzji

EXECUTION TIER (Self-hosted lub tani API - główny workhorse)
├── Qwen2.5-Coder-32B / DeepSeek-Coder-V2
├── Hosting: RunPod/Vast.ai (on-demand) lub Ollama lokalnie
└── Zastosowanie: implementacja, testy, refactoring
```

---

## 3. Scope POC vs Produkcja

### POC (Faza 1) - TO ROBIMY TERAZ

| Komponent | Zakres POC |
|-----------|------------|
| **Backend** | FastAPI + PostgreSQL + Redis |
| **LLM Planning** | 1 provider (Anthropic Claude) |
| **LLM Execution** | Ollama lokalnie LUB OpenRouter API |
| **Adapter** | Tylko CrewAI |
| **Frontend** | TaskInput + TaskBoard + CostDashboard |
| **Deploy** | docker-compose tylko |

### ODŁOŻONE NA PÓŹNIEJ

- LangGraph, AutoGen, Agency Swarm adaptery (Faza 2-3)
- RunPod/Vast.ai GPU management (Faza 2)
- Terraform/Kubernetes (Faza 3)
- Monitoring Prometheus/Grafana (Faza 3)

---

## 4. Kryteria Sukcesu POC

- [ ] `POST /tasks/decompose` → zwraca `TaskDecomposition` JSON w <10s
- [ ] `POST /tasks/{id}/execute` → uruchamia agenta CrewAI
- [ ] WebSocket/SSE → frontend widzi status i logi w real-time
- [ ] Koszt decomposera < $0.10 / zadanie
- [ ] 3-5 scenariuszy demo działa end-to-end

---

## 5. Struktura Projektu (Uproszczona dla POC)

```
agent-orchestrator/
├── docker-compose.yml          # Lokalne środowisko
├── .env.example                # Template zmiennych
├── Makefile                    # Komendy dev
│
├── backend/
│   ├── pyproject.toml
│   ├── alembic/                # DB migrations
│   ├── app/
│   │   ├── main.py             # FastAPI entry + CORS
│   │   ├── config.py           # Pydantic settings
│   │   ├── dependencies.py     # DI + Auth
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── tasks.py    # CRUD + decompose + execute
│   │   │   │   ├── health.py   # Health checks
│   │   │   │   └── costs.py    # Cost summary
│   │   │   └── websockets/
│   │   │       └── progress.py # Real-time updates
│   │   │
│   │   ├── core/
│   │   │   ├── task_decomposer.py
│   │   │   ├── execution_engine.py
│   │   │   └── cost_tracker.py
│   │   │
│   │   ├── adapters/
│   │   │   ├── base.py         # Abstract adapter
│   │   │   └── crewai_adapter.py
│   │   │
│   │   ├── llm/
│   │   │   ├── router.py       # Routing między LLM
│   │   │   └── providers/
│   │   │       ├── anthropic.py
│   │   │       └── openai_compatible.py  # Ollama/OpenRouter
│   │   │
│   │   ├── models/             # SQLAlchemy
│   │   │   ├── task.py
│   │   │   └── execution.py
│   │   │
│   │   └── schemas/            # Pydantic
│   │       ├── task.py
│   │       └── execution.py
│   │
│   └── tests/
│
└── frontend/
    ├── package.json
    ├── src/
    │   ├── App.tsx
    │   ├── api.ts              # Axios client
    │   ├── components/
    │   │   ├── TaskInput.tsx
    │   │   ├── TaskBoard.tsx
    │   │   └── CostDashboard.tsx
    │   ├── hooks/
    │   │   └── useWebSocket.ts
    │   └── types/
    │       └── index.ts
    └── Dockerfile
```

---

## 6. Kluczowe Implementacje

### 6.1 Task Decomposer

```python
# backend/app/core/task_decomposer.py

from pydantic import BaseModel
from typing import List
from app.llm.router import LLMRouter

class SubTask(BaseModel):
    id: str
    title: str
    description: str
    complexity: str  # "simple" | "medium" | "complex"
    dependencies: List[str]
    acceptance_criteria: List[str]

class TaskDecomposition(BaseModel):
    original_task: str
    subtasks: List[SubTask]
    execution_order: List[List[str]]  # Grupy równoległych tasków
    estimated_cost_usd: float

class TaskDecomposer:
    PROMPT = '''
    Rozłóż poniższe zadanie na mniejsze, wykonalne subtaski.

    ZASADY:
    1. Każdy subtask powinien być wykonalny w <30 min
    2. Określ zależności między taskami
    3. Subtaski "simple"/"medium" → execution LLM, "complex" → może wymagać review

    ZADANIE: {task}

    Odpowiedz TYLKO jako JSON zgodny ze schematem TaskDecomposition.
    '''

    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router

    async def decompose(self, task: str) -> TaskDecomposition:
        # Użyj instructor lub pydantic structured output
        response = await self.llm.planning_call(
            prompt=self.PROMPT.format(task=task),
            response_model=TaskDecomposition
        )
        return response
```

### 6.2 LLM Router (z poprawkami)

```python
# backend/app/llm/router.py

from enum import Enum
from typing import Optional, Type
from pydantic import BaseModel

class LLMTier(Enum):
    PLANNING = "planning"
    EXECUTION = "execution"

class LLMRouter:
    def __init__(
        self,
        planning_client,      # DI - łatwe mockowanie
        execution_client,
        cost_tracker
    ):
        self.planning_client = planning_client
        self.execution_client = execution_client
        self.cost_tracker = cost_tracker

    async def planning_call(
        self,
        prompt: str,
        response_model: Optional[Type[BaseModel]] = None,
        max_tokens: int = 2000
    ) -> BaseModel | str:
        """Cloud LLM - używaj oszczędnie"""
        input_tokens = self._estimate_tokens(prompt)

        response = await self.planning_client.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            response_model=response_model
        )

        output_tokens = self._estimate_tokens(str(response))
        await self.cost_tracker.log(
            tier=LLMTier.PLANNING,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )

        return response

    async def execution_call(self, prompt: str, max_tokens: int = 4000) -> str:
        """Self-hosted LLM - główny workhorse"""
        response = await self.execution_client.generate(
            prompt=prompt,
            max_tokens=max_tokens
        )

        # Execution jest tani/darmowy, logujemy tylko dla statystyk
        await self.cost_tracker.log(
            tier=LLMTier.EXECUTION,
            input_tokens=self._estimate_tokens(prompt),
            output_tokens=self._estimate_tokens(response),
            cost_usd=0.0
        )

        return response

    def _estimate_tokens(self, text: str) -> int:
        """Przybliżona estymacja: ~4 znaki = 1 token"""
        return len(text) // 4
```

### 6.3 CrewAI Adapter (z naprawionym async)

```python
# backend/app/adapters/crewai_adapter.py

import asyncio
from concurrent.futures import ThreadPoolExecutor
from crewai import Agent, Task, Crew, Process
from app.adapters.base import BaseAdapter, AgentConfig, TaskResult

class CrewAIAdapter(BaseAdapter):

    def __init__(self, llm_router):
        super().__init__(llm_router)
        self._executor = ThreadPoolExecutor(max_workers=4)

    @property
    def name(self) -> str:
        return "crewai"

    async def create_agent(self, config: AgentConfig) -> Agent:
        return Agent(
            role=config.role,
            goal=config.goal,
            backstory=config.backstory or f"Expert {config.role}",
            llm=self._create_sync_llm_wrapper(config.llm_tier),
            verbose=True
        )

    def _create_sync_llm_wrapper(self, tier: str):
        """Wrapper dla CrewAI (sync) -> nasz router (async)"""
        from langchain.llms.base import LLM

        router = self.llm

        class SyncRouterLLM(LLM):
            @property
            def _llm_type(self) -> str:
                return "router"

            def _call(self, prompt: str, **kwargs) -> str:
                # Uruchom async w nowym event loopie w thread pool
                # Bezpieczne - nie koliduje z głównym event loopem
                loop = asyncio.new_event_loop()
                try:
                    if tier == "planning":
                        return loop.run_until_complete(router.planning_call(prompt))
                    else:
                        return loop.run_until_complete(router.execution_call(prompt))
                finally:
                    loop.close()

        return SyncRouterLLM()

    async def execute_task(
        self,
        agent: Agent,
        task_description: str,
        context: dict = None
    ) -> TaskResult:
        import time
        start = time.time()

        task = Task(
            description=task_description,
            agent=agent,
            expected_output="Task completed with deliverables"
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        # CrewAI kickoff() jest sync - uruchom w thread pool
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self._executor,
                crew.kickoff
            )
            return TaskResult(
                success=True,
                output=result,
                execution_time_seconds=time.time() - start
            )
        except Exception as e:
            return TaskResult(
                success=False,
                output=str(e),
                logs=[f"Error: {e}"],
                execution_time_seconds=time.time() - start
            )
```

### 6.4 Cost Tracker

```python
# backend/app/core/cost_tracker.py

from datetime import datetime, date
from typing import Optional
from app.llm.router import LLMTier

# Ceny per 1M tokenów (przykładowe)
PRICING = {
    "anthropic": {"input": 3.00, "output": 15.00},  # Claude 3.5 Sonnet
    "openai": {"input": 2.50, "output": 10.00},     # GPT-4o
}

class CostTracker:
    def __init__(self, redis_client=None, db_session=None):
        self.redis = redis_client
        self.db = db_session
        self.daily_budget = 5.0  # USD

    async def log(
        self,
        tier: LLMTier,
        input_tokens: int,
        output_tokens: int,
        provider: str = "anthropic",
        cost_usd: Optional[float] = None
    ):
        if cost_usd is None and tier == LLMTier.PLANNING:
            pricing = PRICING.get(provider, PRICING["anthropic"])
            cost_usd = (
                (input_tokens / 1_000_000) * pricing["input"] +
                (output_tokens / 1_000_000) * pricing["output"]
            )

        today = date.today().isoformat()

        if self.redis:
            await self.redis.incrbyfloat(f"cost:{today}:cloud", cost_usd or 0)
            await self.redis.incrby(f"tokens:{today}:input", input_tokens)
            await self.redis.incrby(f"tokens:{today}:output", output_tokens)

    async def get_daily_summary(self) -> dict:
        today = date.today().isoformat()

        if self.redis:
            cloud_cost = float(await self.redis.get(f"cost:{today}:cloud") or 0)
            return {
                "today_cloud": cloud_cost,
                "budget_remaining": self.daily_budget - cloud_cost,
                "budget_percent_used": (cloud_cost / self.daily_budget) * 100
            }

        return {"today_cloud": 0, "budget_remaining": self.daily_budget}

    async def is_budget_exceeded(self) -> bool:
        summary = await self.get_daily_summary()
        return summary["today_cloud"] >= self.daily_budget
```

---

## 7. API Endpoints

### 7.1 Kontrakty

```
POST /tasks/decompose
  Input:  { "description": "string" }
  Output: TaskDecomposition

POST /tasks/{id}/execute
  Output: { "execution_id": "string" }

GET /tasks/{id}
  Output: Task with status and subtasks

GET /executions/{id}
  Output: Execution with logs

GET /costs/summary
  Output: { "today_cloud": float, "budget_remaining": float, ... }

WebSocket /ws/tasks/{id}
  Events: { "type": "status"|"log"|"complete", "data": ... }

GET /health
  Output: { "status": "healthy"|"unhealthy", "checks": {...} }
```

### 7.2 Schematy Błędów

```json
{
  "error": {
    "code": "BUDGET_EXCEEDED",
    "message": "Daily cloud LLM budget exceeded",
    "details": { "current": 5.12, "limit": 5.00 }
  }
}
```

---

## 8. Docker Compose (POC)

```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/orchestrator
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - EXECUTION_LLM_URL=${EXECUTION_LLM_URL:-http://host.docker.internal:11434}
    depends_on:
      - db
      - redis
    command: uvicorn app.main:app --reload --host 0.0.0.0

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
      - POSTGRES_DB=orchestrator
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000

volumes:
  postgres_data:
  redis_data:
```

---

## 9. Checklist Implementacji

### KRYTYCZNE (bez tego POC nie działa)

- [ ] Struktura projektu + pyproject.toml + package.json
- [ ] FastAPI main.py z CORS
- [ ] Pydantic schemas (Task, SubTask, Execution)
- [ ] SQLAlchemy models + Alembic setup
- [ ] LLMRouter z DI
- [ ] Anthropic client (planning)
- [ ] OpenAI-compatible client (execution - Ollama)
- [ ] CostTracker
- [ ] TaskDecomposer
- [ ] CrewAI Adapter (z poprawnym async)
- [ ] API routes: /tasks/decompose, /tasks/{id}
- [ ] Basic API key authentication
- [ ] docker-compose.yml

### WYSOKI PRIORYTET (potrzebne do demo)

- [ ] WebSocket dla real-time updates
- [ ] Health check endpoint
- [ ] /costs/summary endpoint
- [ ] Frontend: TaskInput component
- [ ] Frontend: TaskBoard component
- [ ] Frontend: api.ts (Axios client)
- [ ] Frontend: TypeScript types
- [ ] Logging configuration (structlog)
- [ ] .env.example
- [ ] Basic tests dla decomposera

### ŚREDNI PRIORYTET (nice to have)

- [ ] CostDashboard frontend
- [ ] Budget alerts (Slack/email)
- [ ] Retry logic z exponential backoff
- [ ] Response cache (Redis)
- [ ] Task cancellation endpoint
- [ ] Error boundaries w frontend

### NISKI PRIORYTET (Faza 2+)

- [ ] RunPod integration
- [ ] Dodatkowe adaptery (LangGraph, AutoGen)
- [ ] Terraform
- [ ] Kubernetes
- [ ] Prometheus/Grafana

---

## 10. Znane Ryzyka i Mitygacje

| Ryzyko | Mitygacja |
|--------|-----------|
| Cold start execution LLM | Użyj Ollama lokalnie dla dev, pre-warm w prod |
| CrewAI async/sync conflict | ThreadPoolExecutor wrapper (już w planie) |
| Przekroczenie budżetu cloud | CostTracker + hard limit + alerts |
| Niespójny JSON z LLM | Użyj `instructor` library dla structured output |
| Framework version conflicts | Pinuj wersje w pyproject.toml |

---

## 11. Technologie i Wersje

```toml
# backend/pyproject.toml
[project]
requires-python = ">=3.11"

[project.dependencies]
fastapi = ">=0.109"
uvicorn = ">=0.27"
pydantic = ">=2.6"
sqlalchemy = ">=2.0"
alembic = ">=1.13"
redis = ">=5.0"
httpx = ">=0.26"
crewai = ">=0.28"
instructor = ">=0.5"
structlog = ">=24.1"
tenacity = ">=8.2"

[project.optional-dependencies]
dev = ["pytest", "pytest-asyncio", "pytest-cov"]
```

```json
// frontend/package.json
{
  "dependencies": {
    "react": "^18.2",
    "@tanstack/react-query": "^5.17",
    "axios": "^1.6",
    "zustand": "^4.5"
  }
}
```

---

## 12. Następne Kroki

1. **Inicjalizacja projektu** - struktura katalogów, dependencies
2. **Backend core** - LLMRouter, TaskDecomposer, CostTracker
3. **API endpoints** - routes + schemas
4. **CrewAI adapter** - działająca integracja
5. **Frontend basic** - TaskInput + TaskBoard
6. **Integracja** - end-to-end flow
7. **Testy** - unit + integration
8. **Demo** - 3-5 scenariuszy

---

*Dokument scalony z: plan.md, plan_uwagi.md, plan_uwagi2.md, plan_uwagi3.md*
*Data: 2026-01-08*

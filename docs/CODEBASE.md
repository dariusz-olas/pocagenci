# Mapa Kodu - Agent Orchestrator

> **Cel dokumentu:** Szybka nawigacja po kodzie dla asystentów AI i nowych developerów.

---

## Struktura Katalogów

```
agent-orchestrator/
├── backend/                    # Python FastAPI backend
│   ├── app/                   # Kod aplikacji
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Pydantic Settings
│   │   ├── dependencies.py   # Dependency Injection
│   │   ├── logging_config.py # Strukturalne logowanie
│   │   │
│   │   ├── api/              # Warstwa API
│   │   │   ├── __init__.py
│   │   │   ├── routes/       # REST endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   ├── tasks.py      # /tasks/*
│   │   │   │   ├── executions.py # /executions/*
│   │   │   │   ├── costs.py      # /costs/*
│   │   │   │   └── health.py     # /health
│   │   │   └── websockets/   # WebSocket handlers
│   │   │       ├── __init__.py
│   │   │       └── progress.py   # /ws/tasks/{id}
│   │   │
│   │   ├── core/             # Logika biznesowa
│   │   │   ├── __init__.py
│   │   │   ├── task_decomposer.py  # Dekompozycja zadań
│   │   │   ├── execution_engine.py # Wykonywanie zadań
│   │   │   └── cost_tracker.py     # Śledzenie kosztów
│   │   │
│   │   ├── llm/              # Integracja z LLM
│   │   │   ├── __init__.py
│   │   │   ├── router.py         # Routing planning/execution
│   │   │   └── providers/        # Providery LLM
│   │   │       ├── __init__.py
│   │   │       ├── anthropic.py      # Claude
│   │   │       └── openai_compatible.py # Ollama/OpenRouter
│   │   │
│   │   ├── adapters/         # Adaptery frameworków
│   │   │   ├── __init__.py
│   │   │   ├── base.py           # Abstract base class
│   │   │   └── crewai_adapter.py # Implementacja CrewAI
│   │   │
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── base.py           # Base model, session
│   │   │   ├── task.py           # Task, SubTask
│   │   │   └── execution.py      # Execution
│   │   │
│   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── task.py           # TaskRequest, TaskResponse
│   │   │   ├── execution.py      # ExecutionRequest/Response
│   │   │   └── cost.py           # CostSummary
│   │   │
│   │   └── middleware/       # Middleware
│   │       ├── __init__.py
│   │       └── rate_limiter.py   # Rate limiting
│   │
│   ├── tests/                # Testy
│   │   ├── __init__.py
│   │   ├── conftest.py           # Fixtures
│   │   ├── test_api_tasks.py     # Testy API
│   │   ├── test_task_decomposer.py
│   │   └── test_cost_tracker.py
│   │
│   ├── alembic/              # Migracje bazy danych
│   │   ├── env.py
│   │   └── versions/
│   │       └── 001_initial.py
│   │
│   ├── pyproject.toml        # Dependencies Python
│   ├── Dockerfile
│   └── .env.example
│
└── frontend/                  # React TypeScript frontend
    ├── src/
    │   ├── main.tsx          # React entry point
    │   ├── App.tsx           # Główny komponent
    │   ├── api.ts            # Axios API client
    │   │
    │   ├── components/       # UI komponenty
    │   │   ├── TaskInput.tsx     # Formularz zadania
    │   │   ├── TaskBoard.tsx     # Lista zadań
    │   │   └── CostDashboard.tsx # Dashboard kosztów
    │   │
    │   ├── hooks/            # Custom hooks
    │   │   └── useWebSocket.ts   # WebSocket hook
    │   │
    │   └── types/            # TypeScript types
    │       └── index.ts
    │
    ├── package.json
    ├── vite.config.ts
    └── Dockerfile
```

---

## Kluczowe Pliki - Quick Reference

### Backend Entry Points

| Plik | Odpowiedzialność | Kiedy modyfikować |
|------|------------------|-------------------|
| `app/main.py` | FastAPI app, middleware, CORS | Dodawanie middleware, zmiana CORS |
| `app/config.py` | Zmienne środowiskowe | Nowe ustawienia konfiguracyjne |
| `app/dependencies.py` | Dependency Injection | Nowe serwisy, zależności |

### Core Business Logic

| Plik | Odpowiedzialność | Kiedy modyfikować |
|------|------------------|-------------------|
| `app/core/task_decomposer.py` | Dekompozycja zadań przez LLM | Zmiana promptu, formatu output |
| `app/core/execution_engine.py` | Wykonywanie zadań | Flow wykonania, callbacks |
| `app/core/cost_tracker.py` | Śledzenie kosztów LLM | Pricing, budżety, raporty |

### API Routes

| Plik | Endpointy | Kiedy modyfikować |
|------|-----------|-------------------|
| `app/api/routes/tasks.py` | `/tasks/*` | CRUD zadań, dekompozycja |
| `app/api/routes/executions.py` | `/executions/*` | Status wykonania |
| `app/api/routes/costs.py` | `/costs/*` | Raporty kosztów |
| `app/api/routes/health.py` | `/health` | Health checks |
| `app/api/websockets/progress.py` | `/ws/tasks/{id}` | Real-time updates |

### LLM Integration

| Plik | Odpowiedzialność | Kiedy modyfikować |
|------|------------------|-------------------|
| `app/llm/router.py` | Routing między planning/execution LLM | Strategia routingu |
| `app/llm/providers/anthropic.py` | Klient Claude | Parametry API Anthropic |
| `app/llm/providers/openai_compatible.py` | Ollama/OpenRouter | Parametry API OpenAI-compatible |

### Data Models

| Plik | Modele | Kiedy modyfikować |
|------|--------|-------------------|
| `app/models/task.py` | Task, SubTask | Struktura zadań w DB |
| `app/models/execution.py` | Execution | Struktura wykonania w DB |
| `app/schemas/task.py` | TaskRequest/Response | API contracts |
| `app/schemas/execution.py` | ExecutionRequest/Response | API contracts |
| `app/schemas/cost.py` | CostSummary | Struktura raportu kosztów |

### Frontend

| Plik | Odpowiedzialność | Kiedy modyfikować |
|------|------------------|-------------------|
| `src/App.tsx` | Główny layout, routing | Struktura UI |
| `src/api.ts` | API client (Axios) | Nowe wywołania API |
| `src/types/index.ts` | TypeScript interfaces | Zmiana kontraktów API |
| `src/components/TaskInput.tsx` | Formularz zadania | UI wprowadzania |
| `src/components/TaskBoard.tsx` | Lista zadań | Wyświetlanie zadań |
| `src/components/CostDashboard.tsx` | Dashboard kosztów | Wizualizacja kosztów |
| `src/hooks/useWebSocket.ts` | WebSocket hook | Real-time komunikacja |

---

## Konwencje Nazewnictwa

### Python (Backend)

```python
# Pliki: snake_case.py
task_decomposer.py
cost_tracker.py

# Klasy: PascalCase
class TaskDecomposer:
class CostTracker:

# Funkcje/metody: snake_case
def decompose_task():
async def get_daily_summary():

# Zmienne: snake_case
task_id = "123"
daily_budget = 5.0

# Stałe: UPPER_SNAKE_CASE
PRICING = {...}
DEFAULT_TIMEOUT = 30

# Pydantic models: PascalCase z sufiksem
class TaskRequest(BaseModel):    # Request DTO
class TaskResponse(BaseModel):   # Response DTO
class SubTaskCreate(BaseModel):  # Create DTO
```

### TypeScript (Frontend)

```typescript
// Pliki komponentów: PascalCase.tsx
TaskInput.tsx
TaskBoard.tsx

// Pliki utility: camelCase.ts
api.ts
useWebSocket.ts

// Interfejsy: PascalCase z prefiksem I (opcjonalnie)
interface Task { }
interface SubTask { }

// Typy: PascalCase
type TaskStatus = 'pending' | 'completed';

// Funkcje/zmienne: camelCase
const fetchTasks = () => {};
const taskList = [];

// Komponenty: PascalCase
const TaskInput: React.FC = () => {};
```

---

## Wzorce Projektowe w Kodzie

### 1. Dependency Injection (Backend)

```python
# backend/app/dependencies.py
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_llm_router(settings: Settings = Depends(get_settings)) -> LLMRouter:
    return LLMRouter(
        planning_client=AnthropicClient(settings.anthropic_api_key),
        execution_client=OpenAICompatibleClient(settings.execution_llm_url),
        cost_tracker=get_cost_tracker()
    )

# Użycie w route:
@router.post("/decompose")
async def decompose(
    request: TaskRequest,
    llm_router: LLMRouter = Depends(get_llm_router)
):
    ...
```

### 2. Strategy Pattern (Adapters)

```python
# backend/app/adapters/base.py
class BaseAdapter(ABC):
    @abstractmethod
    async def execute_task(self, agent, task, context) -> TaskResult:
        pass

# backend/app/adapters/crewai_adapter.py
class CrewAIAdapter(BaseAdapter):
    async def execute_task(self, agent, task, context) -> TaskResult:
        # CrewAI specific implementation
        ...
```

### 3. Repository Pattern (Implicit via SQLAlchemy)

```python
# Pobieranie z bazy
async with get_db() as session:
    result = await session.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
```

### 4. Observer Pattern (WebSocket)

```python
# backend/app/api/websockets/progress.py
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def broadcast(self, task_id: str, message: dict):
        for connection in self.active_connections.get(task_id, []):
            await connection.send_json(message)
```

---

## Ważne Zależności

### Backend (pyproject.toml)

| Pakiet | Wersja | Cel |
|--------|--------|-----|
| `fastapi` | >=0.109 | Web framework |
| `uvicorn` | >=0.27 | ASGI server |
| `pydantic` | >=2.6 | Walidacja, schemas |
| `sqlalchemy` | >=2.0 | ORM |
| `alembic` | >=1.13 | Migracje DB |
| `redis` | >=5.0 | Cache, pub/sub |
| `httpx` | >=0.26 | HTTP client (async) |
| `crewai` | >=0.28 | Agent framework |
| `instructor` | >=0.5 | Structured LLM output |
| `structlog` | >=24.1 | Logowanie |
| `tenacity` | >=8.2 | Retry logic |

### Frontend (package.json)

| Pakiet | Wersja | Cel |
|--------|--------|-----|
| `react` | ^18.2 | UI library |
| `@tanstack/react-query` | ^5.17 | Data fetching |
| `axios` | ^1.6 | HTTP client |
| `zustand` | ^4.5 | State management |
| `typescript` | ^5.0 | Type safety |
| `vite` | ^5.0 | Build tool |

---

## Konfiguracja i Środowisko

### Zmienne środowiskowe (backend/.env)

```bash
# Wymagane
API_KEY=your-32-char-api-key
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379

# Opcjonalne
CORS_ORIGINS='["http://localhost:3000"]'
DAILY_BUDGET_USD=5.0
EXECUTION_LLM_URL=http://localhost:11434/v1
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Zmienne środowiskowe (frontend)

```bash
VITE_API_URL=http://localhost:8000
```

---

## Migracje Bazy Danych

```bash
# Tworzenie nowej migracji
cd backend
alembic revision --autogenerate -m "Add new column"

# Aplikowanie migracji
alembic upgrade head

# Cofanie migracji
alembic downgrade -1

# Historia
alembic history
```

**Lokalizacja migracji:** `backend/alembic/versions/`

---

## Testy

### Struktura testów

```
backend/tests/
├── conftest.py              # Fixtures (db session, client, mocks)
├── test_api_tasks.py        # Testy API /tasks
├── test_task_decomposer.py  # Unit testy TaskDecomposer
└── test_cost_tracker.py     # Unit testy CostTracker
```

### Uruchamianie testów

```bash
# Wszystkie testy
cd backend && pytest

# Z coverage
pytest --cov=app --cov-report=html

# Konkretny plik
pytest tests/test_api_tasks.py

# Konkretny test
pytest tests/test_api_tasks.py::test_decompose_task
```

---

## Często Modyfikowane Miejsca

### Dodawanie nowego endpointu

1. `app/schemas/` - dodaj Pydantic models
2. `app/api/routes/` - dodaj route
3. `app/api/routes/__init__.py` - zarejestruj router
4. `frontend/src/api.ts` - dodaj wywołanie API
5. `frontend/src/types/index.ts` - dodaj TypeScript types

### Zmiana modelu danych

1. `app/models/` - modyfikuj SQLAlchemy model
2. `alembic revision --autogenerate -m "description"` - generuj migrację
3. `app/schemas/` - zaktualizuj Pydantic schemas
4. `frontend/src/types/` - zaktualizuj TypeScript types

### Dodawanie nowego adaptera

1. `app/adapters/new_adapter.py` - implementuj BaseAdapter
2. `app/dependencies.py` - dodaj factory
3. `app/config.py` - dodaj konfigurację jeśli potrzebna

---

## Powiązane dokumenty

- [Architektura systemu](ARCHITECTURE.md)
- [Dokumentacja API](API.md)
- [Wytyczne developmentu](DEVELOPMENT.md)
- [Dokumentacja testów](TESTING.md)

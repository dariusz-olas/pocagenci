# Agent Orchestrator - Szczegółowy Plan Zadań

> **CEL DOKUMENTU**: Lista atomowych zadań do wykonania przez Claude Code (w tym Haiku 4.5).
> Każde zadanie jest samodzielne, ma jasne kryteria akceptacji i konkretne pliki do utworzenia.

---

## Jak używać tego dokumentu

1. **Wybierz zadanie** - zacznij od pierwszego nieukończonego `[ ]`
2. **Sprawdź zależności** - upewnij się, że zadania w `WYMAGA` są ukończone
3. **Wykonaj instrukcje** - postępuj dokładnie według opisu
4. **Oznacz jako ukończone** - zmień `[ ]` na `[x]`
5. **Przejdź do następnego** - kontynuuj sekwencyjnie

**Format zadania:**
```
### [NUMER] Nazwa zadania
- **Plik(i)**: ścieżki do utworzenia/edycji
- **Wymaga**: numery zadań-zależności (lub "brak")
- **Opis**: co dokładnie zrobić
- **Kryteria akceptacji**: jak sprawdzić, że zadanie jest ukończone
```

---

## FAZA 0: Setup Projektu

> Tworzenie struktury katalogów i plików konfiguracyjnych.
> **Szacowany czas**: 30-45 min | **Zadania**: 0.1 - 0.8

---

### [ ] 0.1 Utworzenie głównej struktury katalogów

- **Plik(i)**: Katalogi (nie pliki)
- **Wymaga**: brak
- **Opis**: Utwórz podstawową strukturę katalogów projektu.

**Polecenie do wykonania:**
```bash
mkdir -p agent-orchestrator/{backend/{app/{api/routes,api/websockets,core,adapters,llm/providers,models,schemas},tests,alembic/versions},frontend/{src/{components,hooks,types}}}
```

**Kryteria akceptacji:**
- [ ] Katalog `agent-orchestrator/` istnieje
- [ ] Katalog `agent-orchestrator/backend/app/` zawiera: `api/`, `core/`, `adapters/`, `llm/`, `models/`, `schemas/`
- [ ] Katalog `agent-orchestrator/frontend/src/` zawiera: `components/`, `hooks/`, `types/`

---

### [ ] 0.2 Utworzenie pliku .env.example

- **Plik(i)**: `agent-orchestrator/.env.example`
- **Wymaga**: 0.1
- **Opis**: Utwórz template zmiennych środowiskowych.

**Zawartość pliku:**
```env
# === LLM API Keys ===
ANTHROPIC_API_KEY=sk-ant-xxxx

# === Execution LLM (Ollama lub OpenRouter) ===
EXECUTION_LLM_URL=http://localhost:11434
EXECUTION_LLM_MODEL=qwen2.5-coder:32b
# Opcjonalnie dla OpenRouter:
# OPENROUTER_API_KEY=sk-or-xxxx

# === Database ===
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/orchestrator
POSTGRES_PASSWORD=postgres

# === Redis ===
REDIS_URL=redis://localhost:6379

# === API Security ===
API_KEY=dev-api-key-change-in-production

# === Cost Limits ===
DAILY_BUDGET_USD=5.00
```

**Kryteria akceptacji:**
- [ ] Plik `.env.example` istnieje w katalogu głównym projektu
- [ ] Zawiera wszystkie wymagane zmienne (ANTHROPIC_API_KEY, DATABASE_URL, REDIS_URL, API_KEY)

---

### [ ] 0.3 Utworzenie pyproject.toml dla backendu

- **Plik(i)**: `agent-orchestrator/backend/pyproject.toml`
- **Wymaga**: 0.1
- **Opis**: Utwórz plik konfiguracji Python z zależnościami.

**Zawartość pliku:**
```toml
[project]
name = "agent-orchestrator"
version = "0.1.0"
description = "Meta-framework for AI agent orchestration"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.1.0",
    "sqlalchemy>=2.0.25",
    "alembic>=1.13.0",
    "asyncpg>=0.29.0",
    "redis>=5.0.0",
    "httpx>=0.26.0",
    "anthropic>=0.18.0",
    "openai>=1.12.0",
    "crewai>=0.28.0",
    "instructor>=0.5.0",
    "structlog>=24.1.0",
    "tenacity>=8.2.0",
    "python-multipart>=0.0.9",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Kryteria akceptacji:**
- [ ] Plik `pyproject.toml` istnieje w `backend/`
- [ ] Zawiera wszystkie wymagane zależności (fastapi, sqlalchemy, anthropic, crewai, etc.)
- [ ] `requires-python = ">=3.11"`

---

### [ ] 0.4 Utworzenie package.json dla frontendu

- **Plik(i)**: `agent-orchestrator/frontend/package.json`
- **Wymaga**: 0.1
- **Opis**: Utwórz plik konfiguracji npm z zależnościami React.

**Zawartość pliku:**
```json
{
  "name": "agent-orchestrator-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext .ts,.tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-query": "^5.17.0",
    "axios": "^1.6.0",
    "zustand": "^4.5.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "eslint": "^8.56.0",
    "@typescript-eslint/eslint-plugin": "^6.21.0",
    "@typescript-eslint/parser": "^6.21.0"
  }
}
```

**Kryteria akceptacji:**
- [ ] Plik `package.json` istnieje w `frontend/`
- [ ] Zawiera React 18, react-query, axios, zustand
- [ ] Skrypty `dev`, `build` są zdefiniowane

---

### [ ] 0.5 Utworzenie Makefile z komendami deweloperskimi

- **Plik(i)**: `agent-orchestrator/Makefile`
- **Wymaga**: 0.1
- **Opis**: Utwórz Makefile z przydatnymi komendami.

**Zawartość pliku:**
```makefile
.PHONY: install dev test lint clean docker-up docker-down migrate

# === Installation ===
install:
	cd backend && pip install -e ".[dev]"
	cd frontend && npm install

# === Development ===
dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# === Testing ===
test:
	cd backend && pytest -v --cov=app

test-watch:
	cd backend && pytest -v --watch

# === Linting ===
lint:
	cd backend && ruff check app tests
	cd frontend && npm run lint

format:
	cd backend && ruff format app tests

# === Database ===
migrate:
	cd backend && alembic upgrade head

migrate-create:
	cd backend && alembic revision --autogenerate -m "$(name)"

# === Docker ===
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# === Cleanup ===
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
```

**Kryteria akceptacji:**
- [ ] Plik `Makefile` istnieje w katalogu głównym
- [ ] Komendy `make install`, `make dev-backend`, `make test`, `make docker-up` są zdefiniowane

---

### [ ] 0.6 Utworzenie plików __init__.py dla pakietów Python

- **Plik(i)**: Wiele plików `__init__.py`
- **Wymaga**: 0.1
- **Opis**: Utwórz puste pliki `__init__.py` aby Python rozpoznał katalogi jako pakiety.

**Polecenie do wykonania:**
```bash
touch agent-orchestrator/backend/app/__init__.py
touch agent-orchestrator/backend/app/api/__init__.py
touch agent-orchestrator/backend/app/api/routes/__init__.py
touch agent-orchestrator/backend/app/api/websockets/__init__.py
touch agent-orchestrator/backend/app/core/__init__.py
touch agent-orchestrator/backend/app/adapters/__init__.py
touch agent-orchestrator/backend/app/llm/__init__.py
touch agent-orchestrator/backend/app/llm/providers/__init__.py
touch agent-orchestrator/backend/app/models/__init__.py
touch agent-orchestrator/backend/app/schemas/__init__.py
touch agent-orchestrator/backend/tests/__init__.py
```

**Kryteria akceptacji:**
- [ ] Każdy katalog w `backend/app/` zawiera plik `__init__.py`
- [ ] Katalog `backend/tests/` zawiera `__init__.py`

---

### [ ] 0.7 Utworzenie .gitignore

- **Plik(i)**: `agent-orchestrator/.gitignore`
- **Wymaga**: 0.1
- **Opis**: Utwórz plik .gitignore dla projektu Python + Node.js.

**Zawartość pliku:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
.eggs/
*.egg-info/
dist/
build/

# Testing
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build output
frontend/dist/

# Database
*.db
*.sqlite3

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db
```

**Kryteria akceptacji:**
- [ ] Plik `.gitignore` istnieje
- [ ] Zawiera reguły dla Python (`__pycache__`, `.venv`)
- [ ] Zawiera reguły dla Node.js (`node_modules`)
- [ ] Zawiera reguły dla `.env`

---

### [ ] 0.8 Utworzenie README.md projektu

- **Plik(i)**: `agent-orchestrator/README.md`
- **Wymaga**: 0.1
- **Opis**: Utwórz podstawowy plik README z instrukcjami uruchomienia.

**Zawartość pliku:**
```markdown
# Agent Orchestrator

Meta-framework łączący funkcje LangGraph, CrewAI, AutoGen i Agency Swarm z hybrydową architekturą LLM.

## Quick Start

### Wymagania
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Ollama (opcjonalnie, dla lokalnego LLM)

### Instalacja

```bash
# Sklonuj repo
git clone <repo-url>
cd agent-orchestrator

# Skopiuj zmienne środowiskowe
cp .env.example .env
# Edytuj .env i dodaj swoje klucze API

# Zainstaluj zależności
make install

# Uruchom infrastrukturę (Postgres, Redis)
make docker-up

# Uruchom migracje
make migrate

# Uruchom backend (terminal 1)
make dev-backend

# Uruchom frontend (terminal 2)
make dev-frontend
```

### Endpoints

- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Architektura

```
PLANNING TIER (Cloud API)     EXECUTION TIER (Self-hosted)
├── Claude / GPT-4            ├── Qwen2.5-Coder / Ollama
└── <5% wywołań               └── Główny workhorse
```

## Licencja

MIT
```

**Kryteria akceptacji:**
- [ ] Plik `README.md` istnieje
- [ ] Zawiera sekcje: Quick Start, Wymagania, Instalacja, Endpoints

---

## FAZA 1: Backend Core

> Konfiguracja, schematy Pydantic, modele SQLAlchemy, FastAPI setup.
> **Szacowany czas**: 1-2h | **Zadania**: 1.1 - 1.8

---

### [ ] 1.1 Utworzenie pliku konfiguracji (Pydantic Settings)

- **Plik(i)**: `agent-orchestrator/backend/app/config.py`
- **Wymaga**: 0.3, 0.6
- **Opis**: Utwórz klasę Settings z Pydantic do zarządzania konfiguracją z .env.

**Zawartość pliku:**
```python
"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # === Application ===
    app_name: str = "Agent Orchestrator"
    debug: bool = False

    # === Database ===
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/orchestrator"

    # === Redis ===
    redis_url: str = "redis://localhost:6379"

    # === LLM - Planning Tier ===
    anthropic_api_key: str = ""

    # === LLM - Execution Tier ===
    execution_llm_url: str = "http://localhost:11434"
    execution_llm_model: str = "qwen2.5-coder:32b"
    openrouter_api_key: str = ""

    # === Security ===
    api_key: str = "dev-api-key-change-in-production"

    # === Cost Management ===
    daily_budget_usd: float = 5.0


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

**Kryteria akceptacji:**
- [ ] Plik `config.py` istnieje w `backend/app/`
- [ ] Klasa `Settings` dziedziczy po `BaseSettings`
- [ ] Funkcja `get_settings()` jest zdefiniowana z `@lru_cache`
- [ ] Wszystkie zmienne z `.env.example` mają odpowiadające pola

---

### [ ] 1.2 Utworzenie schematów Pydantic - Task

- **Plik(i)**: `agent-orchestrator/backend/app/schemas/task.py`
- **Wymaga**: 0.6
- **Opis**: Utwórz schematy Pydantic dla Task i SubTask (request/response models).

**Zawartość pliku:**
```python
"""Pydantic schemas for Task domain."""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status of a task."""
    PENDING = "pending"
    DECOMPOSING = "decomposing"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class SubTaskComplexity(str, Enum):
    """Complexity level of a subtask."""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


# === Request Schemas ===

class TaskCreateRequest(BaseModel):
    """Request to create a new task."""
    description: str = Field(..., min_length=10, max_length=5000)


class TaskDecomposeRequest(BaseModel):
    """Request to decompose a task into subtasks."""
    description: str = Field(..., min_length=10, max_length=5000)


# === SubTask Schemas ===

class SubTaskBase(BaseModel):
    """Base schema for subtask."""
    title: str
    description: str
    complexity: SubTaskComplexity
    dependencies: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)


class SubTaskResponse(SubTaskBase):
    """Subtask in API response."""
    id: str
    status: TaskStatus = TaskStatus.PENDING


# === Task Schemas ===

class TaskDecomposition(BaseModel):
    """Result of task decomposition by LLM."""
    original_task: str
    subtasks: list[SubTaskBase]
    execution_order: list[list[str]]  # Groups of parallel subtask IDs
    estimated_cost_usd: float = Field(ge=0)


class TaskResponse(BaseModel):
    """Task in API response."""
    id: str
    description: str
    status: TaskStatus
    subtasks: list[SubTaskResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
```

**Kryteria akceptacji:**
- [ ] Plik `schemas/task.py` istnieje
- [ ] Enum `TaskStatus` zawiera: PENDING, DECOMPOSING, READY, IN_PROGRESS, COMPLETED, FAILED
- [ ] Klasa `TaskDecomposition` ma pola: original_task, subtasks, execution_order, estimated_cost_usd
- [ ] Klasa `TaskResponse` ma `model_config = {"from_attributes": True}`

---

### [ ] 1.3 Utworzenie schematów Pydantic - Execution

- **Plik(i)**: `agent-orchestrator/backend/app/schemas/execution.py`
- **Wymaga**: 0.6
- **Opis**: Utwórz schematy Pydantic dla Execution (uruchomienie zadania).

**Zawartość pliku:**
```python
"""Pydantic schemas for Execution domain."""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Status of an execution."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionCreateResponse(BaseModel):
    """Response after starting an execution."""
    execution_id: str
    task_id: str
    status: ExecutionStatus = ExecutionStatus.QUEUED


class ExecutionLogEntry(BaseModel):
    """Single log entry from execution."""
    timestamp: datetime
    level: str  # "info", "warning", "error"
    message: str
    agent: Optional[str] = None


class ExecutionResponse(BaseModel):
    """Execution details in API response."""
    id: str
    task_id: str
    status: ExecutionStatus
    output: Optional[str] = None
    logs: list[ExecutionLogEntry] = Field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time_seconds: Optional[float] = None

    model_config = {"from_attributes": True}


class ExecutionProgress(BaseModel):
    """Real-time progress update via WebSocket."""
    execution_id: str
    type: str  # "status", "log", "complete", "error"
    data: dict
```

**Kryteria akceptacji:**
- [ ] Plik `schemas/execution.py` istnieje
- [ ] Enum `ExecutionStatus` zawiera: QUEUED, RUNNING, COMPLETED, FAILED, CANCELLED
- [ ] Klasa `ExecutionProgress` jest zdefiniowana (dla WebSocket)

---

### [ ] 1.4 Utworzenie schematów Pydantic - Cost

- **Plik(i)**: `agent-orchestrator/backend/app/schemas/cost.py`
- **Wymaga**: 0.6
- **Opis**: Utwórz schematy Pydantic dla Cost tracking.

**Zawartość pliku:**
```python
"""Pydantic schemas for Cost tracking."""

from pydantic import BaseModel, Field


class CostSummary(BaseModel):
    """Daily cost summary."""
    today_cloud_usd: float = Field(ge=0)
    today_tokens_input: int = Field(ge=0)
    today_tokens_output: int = Field(ge=0)
    budget_limit_usd: float = Field(ge=0)
    budget_remaining_usd: float
    budget_percent_used: float = Field(ge=0, le=100)


class CostEntry(BaseModel):
    """Single cost log entry."""
    tier: str  # "planning" or "execution"
    provider: str  # "anthropic", "openai", "ollama"
    input_tokens: int
    output_tokens: int
    cost_usd: float


class BudgetExceededError(BaseModel):
    """Error response when budget is exceeded."""
    error: str = "BUDGET_EXCEEDED"
    message: str = "Daily cloud LLM budget exceeded"
    details: dict  # {"current": 5.12, "limit": 5.00}
```

**Kryteria akceptacji:**
- [ ] Plik `schemas/cost.py` istnieje
- [ ] Klasa `CostSummary` zawiera pola: today_cloud_usd, budget_remaining_usd, budget_percent_used

---

### [ ] 1.5 Eksport schematów w __init__.py

- **Plik(i)**: `agent-orchestrator/backend/app/schemas/__init__.py`
- **Wymaga**: 1.2, 1.3, 1.4
- **Opis**: Wyeksportuj wszystkie schematy z pakietu schemas.

**Zawartość pliku:**
```python
"""Pydantic schemas package."""

from app.schemas.task import (
    TaskStatus,
    SubTaskComplexity,
    TaskCreateRequest,
    TaskDecomposeRequest,
    SubTaskBase,
    SubTaskResponse,
    TaskDecomposition,
    TaskResponse,
)
from app.schemas.execution import (
    ExecutionStatus,
    ExecutionCreateResponse,
    ExecutionLogEntry,
    ExecutionResponse,
    ExecutionProgress,
)
from app.schemas.cost import (
    CostSummary,
    CostEntry,
    BudgetExceededError,
)

__all__ = [
    # Task
    "TaskStatus",
    "SubTaskComplexity",
    "TaskCreateRequest",
    "TaskDecomposeRequest",
    "SubTaskBase",
    "SubTaskResponse",
    "TaskDecomposition",
    "TaskResponse",
    # Execution
    "ExecutionStatus",
    "ExecutionCreateResponse",
    "ExecutionLogEntry",
    "ExecutionResponse",
    "ExecutionProgress",
    # Cost
    "CostSummary",
    "CostEntry",
    "BudgetExceededError",
]
```

**Kryteria akceptacji:**
- [ ] Plik `schemas/__init__.py` eksportuje wszystkie schematy
- [ ] Lista `__all__` zawiera wszystkie eksportowane klasy

---

### [ ] 1.6 Utworzenie modeli SQLAlchemy - Task

- **Plik(i)**: `agent-orchestrator/backend/app/models/task.py`
- **Wymaga**: 0.6
- **Opis**: Utwórz model SQLAlchemy dla Task i SubTask.

**Zawartość pliku:**
```python
"""SQLAlchemy models for Task domain."""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    JSON,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base
from app.schemas.task import TaskStatus, SubTaskComplexity


class Task(Base):
    """Task model - main task submitted by user."""

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False
    )
    decomposition_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, onupdate=datetime.utcnow, nullable=True
    )

    # Relationships
    subtasks: Mapped[list["SubTask"]] = relationship(
        "SubTask", back_populates="parent_task", cascade="all, delete-orphan"
    )
    executions: Mapped[list["Execution"]] = relationship(
        "Execution", back_populates="task", cascade="all, delete-orphan"
    )


class SubTask(Base):
    """SubTask model - decomposed part of a main task."""

    __tablename__ = "subtasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    complexity: Mapped[SubTaskComplexity] = mapped_column(
        SQLEnum(SubTaskComplexity), nullable=False
    )
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False
    )
    dependencies: Mapped[list] = mapped_column(JSON, default=list)
    acceptance_criteria: Mapped[list] = mapped_column(JSON, default=list)
    order_index: Mapped[int] = mapped_column(default=0)

    # Relationships
    parent_task: Mapped["Task"] = relationship("Task", back_populates="subtasks")
```

**Kryteria akceptacji:**
- [ ] Plik `models/task.py` istnieje
- [ ] Model `Task` ma pola: id (UUID), description, status, created_at
- [ ] Model `SubTask` ma relację do `Task` (ForeignKey)
- [ ] Oba modele używają `Mapped` z SQLAlchemy 2.0

---

### [ ] 1.7 Utworzenie modeli SQLAlchemy - Execution + Base

- **Plik(i)**:
  - `agent-orchestrator/backend/app/models/base.py`
  - `agent-orchestrator/backend/app/models/execution.py`
- **Wymaga**: 0.6
- **Opis**: Utwórz bazową klasę modeli i model Execution.

**Zawartość pliku `base.py`:**
```python
"""SQLAlchemy Base model."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass
```

**Zawartość pliku `execution.py`:**
```python
"""SQLAlchemy models for Execution domain."""

import uuid
from datetime import datetime
from sqlalchemy import Text, DateTime, ForeignKey, Float, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base
from app.schemas.execution import ExecutionStatus


class Execution(Base):
    """Execution model - represents a single run of a task."""

    __tablename__ = "executions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False
    )
    status: Mapped[ExecutionStatus] = mapped_column(
        SQLEnum(ExecutionStatus), default=ExecutionStatus.QUEUED, nullable=False
    )
    output: Mapped[str | None] = mapped_column(Text, nullable=True)
    logs: Mapped[list] = mapped_column(JSON, default=list)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    execution_time_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    adapter_name: Mapped[str] = mapped_column(default="crewai")
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="executions")
```

**Kryteria akceptacji:**
- [ ] Plik `models/base.py` istnieje z klasą `Base`
- [ ] Plik `models/execution.py` istnieje
- [ ] Model `Execution` ma relację do `Task`
- [ ] Pola: status, output, logs, started_at, completed_at są zdefiniowane

---

### [ ] 1.8 Eksport modeli i utworzenie głównego FastAPI app

- **Plik(i)**:
  - `agent-orchestrator/backend/app/models/__init__.py`
  - `agent-orchestrator/backend/app/main.py`
- **Wymaga**: 1.6, 1.7, 1.1
- **Opis**: Wyeksportuj modele i utwórz główną aplikację FastAPI.

**Zawartość pliku `models/__init__.py`:**
```python
"""SQLAlchemy models package."""

from app.models.base import Base
from app.models.task import Task, SubTask
from app.models.execution import Execution

__all__ = ["Base", "Task", "SubTask", "Execution"]
```

**Zawartość pliku `main.py`:**
```python
"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup
    settings = get_settings()
    print(f"Starting {settings.app_name}...")
    yield
    # Shutdown
    print("Shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Meta-framework for AI agent orchestration",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint (temporary, will be moved to routes)
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


# Create app instance
app = create_app()
```

**Kryteria akceptacji:**
- [ ] Plik `models/__init__.py` eksportuje Base, Task, SubTask, Execution
- [ ] Plik `main.py` istnieje z funkcją `create_app()`
- [ ] CORS middleware jest skonfigurowany dla localhost:3000
- [ ] Endpoint `/health` zwraca `{"status": "healthy"}`

---

## FAZA 2: LLM Integration

> Integracja z LLM - router, providery Anthropic i OpenAI-compatible.
> **Szacowany czas**: 1-1.5h | **Zadania**: 2.1 - 2.4

---

### [ ] 2.1 Utworzenie Anthropic Provider (Planning Tier)

- **Plik(i)**: `agent-orchestrator/backend/app/llm/providers/anthropic.py`
- **Wymaga**: 1.1
- **Opis**: Utwórz klienta Anthropic dla planning tier (Claude).

**Zawartość pliku:**
```python
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
```

**Kryteria akceptacji:**
- [ ] Plik `llm/providers/anthropic.py` istnieje
- [ ] Klasa `AnthropicProvider` ma metody: `generate()`, `count_tokens()`
- [ ] Obsługuje structured output przez `instructor`
- [ ] Domyślny model to `claude-3-5-sonnet-20241022`

---

### [ ] 2.2 Utworzenie OpenAI-Compatible Provider (Execution Tier)

- **Plik(i)**: `agent-orchestrator/backend/app/llm/providers/openai_compatible.py`
- **Wymaga**: 1.1
- **Opis**: Utwórz klienta kompatybilnego z OpenAI API (Ollama, OpenRouter).

**Zawartość pliku:**
```python
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
```

**Kryteria akceptacji:**
- [ ] Plik `llm/providers/openai_compatible.py` istnieje
- [ ] Klasa `OpenAICompatibleProvider` działa z Ollama (localhost:11434)
- [ ] Metoda `is_available()` sprawdza dostępność serwisu
- [ ] Timeout ustawiony na 120s (długie generowanie)

---

### [ ] 2.3 Utworzenie LLM Router

- **Plik(i)**: `agent-orchestrator/backend/app/llm/router.py`
- **Wymaga**: 2.1, 2.2
- **Opis**: Utwórz router kierujący żądania do odpowiedniego LLM tier.

**Zawartość pliku:**
```python
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
```

**Kryteria akceptacji:**
- [ ] Plik `llm/router.py` istnieje
- [ ] Enum `LLMTier` ma wartości: PLANNING, EXECUTION
- [ ] Metoda `planning_call()` używa Anthropic
- [ ] Metoda `execution_call()` używa OpenAI-compatible
- [ ] Cost tracker jest integrowany

---

### [ ] 2.4 Eksport LLM modułu

- **Plik(i)**:
  - `agent-orchestrator/backend/app/llm/__init__.py`
  - `agent-orchestrator/backend/app/llm/providers/__init__.py`
- **Wymaga**: 2.1, 2.2, 2.3
- **Opis**: Wyeksportuj komponenty LLM.

**Zawartość pliku `llm/__init__.py`:**
```python
"""LLM integration package."""

from app.llm.router import LLMRouter, LLMTier
from app.llm.providers.anthropic import AnthropicProvider
from app.llm.providers.openai_compatible import OpenAICompatibleProvider

__all__ = [
    "LLMRouter",
    "LLMTier",
    "AnthropicProvider",
    "OpenAICompatibleProvider",
]
```

**Zawartość pliku `llm/providers/__init__.py`:**
```python
"""LLM providers package."""

from app.llm.providers.anthropic import AnthropicProvider
from app.llm.providers.openai_compatible import OpenAICompatibleProvider

__all__ = ["AnthropicProvider", "OpenAICompatibleProvider"]
```

**Kryteria akceptacji:**
- [ ] Plik `llm/__init__.py` eksportuje LLMRouter, LLMTier, providery
- [ ] Plik `llm/providers/__init__.py` eksportuje providery

---

## FAZA 3: Core Logic

> Logika biznesowa - TaskDecomposer, CostTracker, ExecutionEngine.
> **Szacowany czas**: 1.5-2h | **Zadania**: 3.1 - 3.4

---

### [ ] 3.1 Utworzenie Cost Tracker

- **Plik(i)**: `agent-orchestrator/backend/app/core/cost_tracker.py`
- **Wymaga**: 2.3
- **Opis**: Utwórz tracker kosztów LLM z Redis storage.

**Zawartość pliku:**
```python
"""Cost tracking for LLM usage."""

from datetime import date
from typing import Optional
from redis.asyncio import Redis

from app.llm.router import LLMTier
from app.schemas.cost import CostSummary

# Pricing per 1M tokens (USD)
PRICING = {
    "anthropic": {"input": 3.00, "output": 15.00},  # Claude 3.5 Sonnet
    "openai": {"input": 2.50, "output": 10.00},     # GPT-4o
    "ollama": {"input": 0.0, "output": 0.0},        # Local - free
}


class CostTracker:
    """Tracks LLM usage costs with Redis backend."""

    def __init__(self, redis: Optional[Redis] = None, daily_budget: float = 5.0):
        self.redis = redis
        self.daily_budget = daily_budget

    async def log(
        self,
        tier: LLMTier,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: Optional[float] = None,
    ) -> None:
        """Log LLM usage and cost.

        Args:
            tier: LLM tier (planning/execution)
            provider: Provider name (anthropic, openai, ollama)
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost_usd: Override cost (for execution tier = 0)
        """
        if cost_usd is None and tier == LLMTier.PLANNING:
            pricing = PRICING.get(provider, PRICING["anthropic"])
            cost_usd = (
                (input_tokens / 1_000_000) * pricing["input"] +
                (output_tokens / 1_000_000) * pricing["output"]
            )
        elif cost_usd is None:
            cost_usd = 0.0

        today = date.today().isoformat()

        if self.redis:
            pipe = self.redis.pipeline()
            pipe.incrbyfloat(f"cost:{today}:cloud", cost_usd)
            pipe.incrby(f"tokens:{today}:input", input_tokens)
            pipe.incrby(f"tokens:{today}:output", output_tokens)
            pipe.expire(f"cost:{today}:cloud", 86400 * 7)  # 7 days TTL
            pipe.expire(f"tokens:{today}:input", 86400 * 7)
            pipe.expire(f"tokens:{today}:output", 86400 * 7)
            await pipe.execute()

    async def get_summary(self) -> CostSummary:
        """Get today's cost summary.

        Returns:
            CostSummary with current usage and budget status
        """
        today = date.today().isoformat()

        if self.redis:
            cloud_cost = float(await self.redis.get(f"cost:{today}:cloud") or 0)
            input_tokens = int(await self.redis.get(f"tokens:{today}:input") or 0)
            output_tokens = int(await self.redis.get(f"tokens:{today}:output") or 0)
        else:
            cloud_cost = 0.0
            input_tokens = 0
            output_tokens = 0

        remaining = self.daily_budget - cloud_cost
        percent_used = (cloud_cost / self.daily_budget * 100) if self.daily_budget > 0 else 0

        return CostSummary(
            today_cloud_usd=round(cloud_cost, 4),
            today_tokens_input=input_tokens,
            today_tokens_output=output_tokens,
            budget_limit_usd=self.daily_budget,
            budget_remaining_usd=round(remaining, 4),
            budget_percent_used=round(percent_used, 2),
        )

    async def is_budget_exceeded(self) -> bool:
        """Check if daily budget is exceeded.

        Returns:
            True if budget exceeded
        """
        summary = await self.get_summary()
        return summary.today_cloud_usd >= self.daily_budget
```

**Kryteria akceptacji:**
- [ ] Plik `core/cost_tracker.py` istnieje
- [ ] Metoda `log()` zapisuje koszty do Redis
- [ ] Metoda `get_summary()` zwraca `CostSummary`
- [ ] Metoda `is_budget_exceeded()` sprawdza limit
- [ ] TTL dla kluczy Redis = 7 dni

---

### [ ] 3.2 Utworzenie Task Decomposer

- **Plik(i)**: `agent-orchestrator/backend/app/core/task_decomposer.py`
- **Wymaga**: 2.3, 1.2
- **Opis**: Utwórz decomposer rozbijający zadania na subtaski.

**Zawartość pliku:**
```python
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
{{
  "original_task": "opis oryginalnego zadania",
  "subtasks": [
    {{
      "title": "krótki tytuł",
      "description": "szczegółowy opis co zrobić",
      "complexity": "simple|medium|complex",
      "dependencies": ["id subtaska od którego zależy"],
      "acceptance_criteria": ["kryterium 1", "kryterium 2"]
    }}
  ],
  "execution_order": [["subtask-1"], ["subtask-2", "subtask-3"], ["subtask-4"]],
  "estimated_cost_usd": 0.05
}}
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
```

**Kryteria akceptacji:**
- [ ] Plik `core/task_decomposer.py` istnieje
- [ ] Metoda `decompose()` używa planning LLM
- [ ] Prompt zawiera jasne instrukcje dla LLM
- [ ] Metoda `validate_decomposition()` sprawdza poprawność

---

### [ ] 3.3 Utworzenie Execution Engine

- **Plik(i)**: `agent-orchestrator/backend/app/core/execution_engine.py`
- **Wymaga**: 3.2, 1.3
- **Opis**: Utwórz silnik wykonujący subtaski przez adaptery.

**Zawartość pliku:**
```python
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
```

**Kryteria akceptacji:**
- [ ] Plik `core/execution_engine.py` istnieje
- [ ] Metoda `execute_subtask()` wykonuje pojedynczy subtask
- [ ] Metoda `execute_task()` wykonuje grupy równolegle
- [ ] Progress callbacks dla WebSocket są obsługiwane
- [ ] Obsługa błędów nie przerywa całej egzekucji

---

### [ ] 3.4 Eksport Core modułu

- **Plik(i)**: `agent-orchestrator/backend/app/core/__init__.py`
- **Wymaga**: 3.1, 3.2, 3.3
- **Opis**: Wyeksportuj komponenty core.

**Zawartość pliku:**
```python
"""Core business logic package."""

from app.core.cost_tracker import CostTracker, PRICING
from app.core.task_decomposer import TaskDecomposer
from app.core.execution_engine import ExecutionEngine

__all__ = [
    "CostTracker",
    "PRICING",
    "TaskDecomposer",
    "ExecutionEngine",
]
```

**Kryteria akceptacji:**
- [ ] Plik `core/__init__.py` eksportuje wszystkie komponenty

---

## FAZA 4: API Endpoints

> FastAPI routes - tasks, executions, costs, health, WebSocket.
> **Szacowany czas**: 1.5-2h | **Zadania**: 4.1 - 4.6

---

### [ ] 4.1 Utworzenie Dependencies (Dependency Injection)

- **Plik(i)**: `agent-orchestrator/backend/app/dependencies.py`
- **Wymaga**: 1.1, 2.3, 3.1
- **Opis**: Utwórz zależności FastAPI dla DI.

**Zawartość pliku:**
```python
"""FastAPI dependencies for dependency injection."""

from typing import AsyncGenerator
from fastapi import Depends, HTTPException, Header, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import Settings, get_settings
from app.llm import LLMRouter, AnthropicProvider, OpenAICompatibleProvider
from app.core import CostTracker, TaskDecomposer

# Global instances (initialized on startup)
_engine = None
_session_factory = None
_redis: Redis | None = None
_llm_router: LLMRouter | None = None
_cost_tracker: CostTracker | None = None


async def init_dependencies(settings: Settings):
    """Initialize all dependencies (called on app startup)."""
    global _engine, _session_factory, _redis, _llm_router, _cost_tracker

    # Database
    _engine = create_async_engine(settings.database_url, echo=settings.debug)
    _session_factory = async_sessionmaker(_engine, expire_on_commit=False)

    # Redis
    _redis = Redis.from_url(settings.redis_url)

    # Cost Tracker
    _cost_tracker = CostTracker(redis=_redis, daily_budget=settings.daily_budget_usd)

    # LLM Providers
    planning_provider = AnthropicProvider(api_key=settings.anthropic_api_key)
    execution_provider = OpenAICompatibleProvider(
        base_url=f"{settings.execution_llm_url}/v1",
        model=settings.execution_llm_model,
    )

    # LLM Router
    _llm_router = LLMRouter(
        planning_provider=planning_provider,
        execution_provider=execution_provider,
        cost_tracker=_cost_tracker,
    )


async def cleanup_dependencies():
    """Cleanup dependencies (called on app shutdown)."""
    global _engine, _redis
    if _redis:
        await _redis.close()
    if _engine:
        await _engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    if _session_factory is None:
        raise RuntimeError("Database not initialized")
    async with _session_factory() as session:
        yield session


def get_redis() -> Redis:
    """Get Redis client."""
    if _redis is None:
        raise RuntimeError("Redis not initialized")
    return _redis


def get_llm_router() -> LLMRouter:
    """Get LLM router."""
    if _llm_router is None:
        raise RuntimeError("LLM Router not initialized")
    return _llm_router


def get_cost_tracker() -> CostTracker:
    """Get cost tracker."""
    if _cost_tracker is None:
        raise RuntimeError("Cost tracker not initialized")
    return _cost_tracker


def get_task_decomposer(
    llm_router: LLMRouter = Depends(get_llm_router),
) -> TaskDecomposer:
    """Get task decomposer."""
    return TaskDecomposer(llm_router)


async def verify_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    settings: Settings = Depends(get_settings),
) -> str:
    """Verify API key from header."""
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return x_api_key
```

**Kryteria akceptacji:**
- [ ] Plik `dependencies.py` istnieje
- [ ] Funkcje `init_dependencies()` i `cleanup_dependencies()` są zdefiniowane
- [ ] `get_db()`, `get_redis()`, `get_llm_router()` są dostępne
- [ ] `verify_api_key()` sprawdza nagłówek X-API-Key

---

### [ ] 4.2 Utworzenie Tasks Routes

- **Plik(i)**: `agent-orchestrator/backend/app/api/routes/tasks.py`
- **Wymaga**: 4.1, 1.2, 3.2
- **Opis**: Utwórz endpointy dla zadań (CRUD, decompose, execute).

**Zawartość pliku:**
```python
"""API routes for task management."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db, get_task_decomposer, get_cost_tracker, verify_api_key
from app.schemas import (
    TaskCreateRequest,
    TaskDecomposeRequest,
    TaskResponse,
    TaskDecomposition,
    TaskStatus,
    ExecutionCreateResponse,
    ExecutionStatus,
)
from app.models import Task, SubTask, Execution
from app.core import TaskDecomposer, CostTracker

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/decompose", response_model=TaskDecomposition)
async def decompose_task(
    request: TaskDecomposeRequest,
    decomposer: TaskDecomposer = Depends(get_task_decomposer),
    cost_tracker: CostTracker = Depends(get_cost_tracker),
    _: str = Depends(verify_api_key),
):
    """Decompose a task into subtasks using planning LLM.

    This endpoint uses the cloud LLM (planning tier) to analyze
    the task and break it down into executable subtasks.
    """
    # Check budget
    if await cost_tracker.is_budget_exceeded():
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "error": "BUDGET_EXCEEDED",
                "message": "Daily cloud LLM budget exceeded",
            },
        )

    try:
        decomposition = await decomposer.decompose(request.description)
        return decomposition
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decomposition failed: {str(e)}",
        )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Create a new task."""
    task = Task(description=request.description, status=TaskStatus.PENDING)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    return TaskResponse(
        id=str(task.id),
        description=task.description,
        status=task.status,
        subtasks=[],
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Get task by ID with subtasks."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    return TaskResponse(
        id=str(task.id),
        description=task.description,
        status=task.status,
        subtasks=[],  # TODO: Load subtasks
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.post("/{task_id}/execute", response_model=ExecutionCreateResponse)
async def execute_task(
    task_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Start task execution.

    Creates an execution record and starts the execution in the background.
    Use WebSocket endpoint to monitor progress.
    """
    # Get task
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    if task.status not in [TaskStatus.READY, TaskStatus.PENDING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task is in {task.status} state, cannot execute",
        )

    # Create execution
    execution = Execution(
        task_id=task.id,
        status=ExecutionStatus.QUEUED,
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)

    # TODO: Add background task to run execution
    # background_tasks.add_task(run_execution, execution.id)

    return ExecutionCreateResponse(
        execution_id=str(execution.id),
        task_id=str(task.id),
        status=ExecutionStatus.QUEUED,
    )
```

**Kryteria akceptacji:**
- [ ] Plik `api/routes/tasks.py` istnieje
- [ ] Endpoint `POST /tasks/decompose` rozbija zadanie
- [ ] Endpoint `POST /tasks` tworzy nowe zadanie
- [ ] Endpoint `GET /tasks/{id}` zwraca zadanie
- [ ] Endpoint `POST /tasks/{id}/execute` startuje wykonanie
- [ ] Wszystkie endpointy wymagają X-API-Key

---

### [ ] 4.3 Utworzenie Costs Routes

- **Plik(i)**: `agent-orchestrator/backend/app/api/routes/costs.py`
- **Wymaga**: 4.1, 3.1
- **Opis**: Utwórz endpoint dla podsumowania kosztów.

**Zawartość pliku:**
```python
"""API routes for cost tracking."""

from fastapi import APIRouter, Depends

from app.dependencies import get_cost_tracker, verify_api_key
from app.schemas import CostSummary
from app.core import CostTracker

router = APIRouter(prefix="/costs", tags=["costs"])


@router.get("/summary", response_model=CostSummary)
async def get_cost_summary(
    cost_tracker: CostTracker = Depends(get_cost_tracker),
    _: str = Depends(verify_api_key),
):
    """Get today's cost summary.

    Returns current cloud LLM usage, token counts, and budget status.
    """
    return await cost_tracker.get_summary()
```

**Kryteria akceptacji:**
- [ ] Plik `api/routes/costs.py` istnieje
- [ ] Endpoint `GET /costs/summary` zwraca `CostSummary`

---

### [ ] 4.4 Utworzenie Health Routes

- **Plik(i)**: `agent-orchestrator/backend/app/api/routes/health.py`
- **Wymaga**: 4.1
- **Opis**: Utwórz endpoint health check ze szczegółami.

**Zawartość pliku:**
```python
"""API routes for health checks."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_redis, get_llm_router
from app.llm import LLMRouter

router = APIRouter(tags=["health"])


class HealthCheck(BaseModel):
    """Health check response."""
    status: str  # "healthy" or "unhealthy"
    checks: dict[str, bool]


@router.get("/health", response_model=HealthCheck)
async def health_check(
    llm_router: LLMRouter = Depends(get_llm_router),
):
    """Check health of all services.

    Returns status of database, Redis, and execution LLM.
    """
    checks = {}

    # Check Redis
    try:
        redis = get_redis()
        await redis.ping()
        checks["redis"] = True
    except Exception:
        checks["redis"] = False

    # Check execution LLM (Ollama)
    try:
        checks["execution_llm"] = await llm_router.is_execution_available()
    except Exception:
        checks["execution_llm"] = False

    # Database check is implicit - if we got here, it's working

    all_healthy = all(checks.values())

    return HealthCheck(
        status="healthy" if all_healthy else "unhealthy",
        checks=checks,
    )


@router.get("/health/live")
async def liveness():
    """Simple liveness probe."""
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness(
    llm_router: LLMRouter = Depends(get_llm_router),
):
    """Readiness probe - checks if service is ready to accept traffic."""
    try:
        redis = get_redis()
        await redis.ping()
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}
```

**Kryteria akceptacji:**
- [ ] Plik `api/routes/health.py` istnieje
- [ ] Endpoint `GET /health` sprawdza Redis i Ollama
- [ ] Endpointy `/health/live` i `/health/ready` dla Kubernetes

---

### [ ] 4.5 Utworzenie WebSocket dla Progress Updates

- **Plik(i)**: `agent-orchestrator/backend/app/api/websockets/progress.py`
- **Wymaga**: 4.1, 1.3
- **Opis**: Utwórz WebSocket endpoint dla real-time updates.

**Zawartość pliku:**
```python
"""WebSocket endpoint for execution progress updates."""

import asyncio
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from redis.asyncio import Redis

from app.dependencies import get_redis
from app.schemas import ExecutionProgress

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for execution updates."""

    def __init__(self):
        # execution_id -> list of websockets
        self.connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, execution_id: str):
        """Accept and store WebSocket connection."""
        await websocket.accept()
        if execution_id not in self.connections:
            self.connections[execution_id] = []
        self.connections[execution_id].append(websocket)

    def disconnect(self, websocket: WebSocket, execution_id: str):
        """Remove WebSocket connection."""
        if execution_id in self.connections:
            self.connections[execution_id].remove(websocket)
            if not self.connections[execution_id]:
                del self.connections[execution_id]

    async def broadcast(self, execution_id: str, message: dict):
        """Broadcast message to all connections for an execution."""
        if execution_id in self.connections:
            for websocket in self.connections[execution_id]:
                try:
                    await websocket.send_json(message)
                except Exception:
                    pass  # Connection might be closed


manager = ConnectionManager()


@router.websocket("/ws/executions/{execution_id}")
async def execution_progress(
    websocket: WebSocket,
    execution_id: UUID,
):
    """WebSocket endpoint for execution progress updates.

    Connect to receive real-time updates about task execution.

    Events:
    - {"type": "status", "data": {"status": "running", "subtask": "..."}}
    - {"type": "log", "data": {"message": "...", "level": "info"}}
    - {"type": "complete", "data": {"status": "completed", "results": {...}}}
    - {"type": "error", "data": {"error": "..."}}
    """
    execution_id_str = str(execution_id)

    await manager.connect(websocket, execution_id_str)

    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connected",
            "data": {"execution_id": execution_id_str},
        })

        # Keep connection alive and wait for messages
        while True:
            try:
                # Wait for any message (ping/pong or close)
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0,
                )
                # Handle ping
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_text("ping")

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket, execution_id_str)


async def send_progress_update(execution_id: str, progress: ExecutionProgress):
    """Send progress update to all connected clients.

    Called by ExecutionEngine during task execution.
    """
    await manager.broadcast(execution_id, progress.model_dump())
```

**Kryteria akceptacji:**
- [ ] Plik `api/websockets/progress.py` istnieje
- [ ] Klasa `ConnectionManager` zarządza połączeniami
- [ ] Endpoint `WS /ws/executions/{id}` akceptuje połączenia
- [ ] Funkcja `send_progress_update()` wysyła aktualizacje

---

### [ ] 4.6 Rejestracja Routes w main.py

- **Plik(i)**: `agent-orchestrator/backend/app/main.py` (EDYCJA)
- **Wymaga**: 4.1, 4.2, 4.3, 4.4, 4.5
- **Opis**: Zarejestruj wszystkie routery w aplikacji FastAPI.

**Zmodyfikowana zawartość `main.py`:**
```python
"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.dependencies import init_dependencies, cleanup_dependencies
from app.api.routes import tasks, costs, health
from app.api.websockets import progress


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    settings = get_settings()
    print(f"Starting {settings.app_name}...")

    # Initialize dependencies
    await init_dependencies(settings)

    yield

    # Cleanup
    await cleanup_dependencies()
    print("Shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Meta-framework for AI agent orchestration",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health.router)
    app.include_router(tasks.router, prefix="/api/v1")
    app.include_router(costs.router, prefix="/api/v1")
    app.include_router(progress.router)

    return app


# Create app instance
app = create_app()
```

**Kryteria akceptacji:**
- [ ] `main.py` importuje wszystkie routery
- [ ] `init_dependencies()` wywoływane przy starcie
- [ ] `cleanup_dependencies()` wywoływane przy zamknięciu
- [ ] Routery zarejestrowane z prefiksem `/api/v1`

---

## FAZA 5: CrewAI Adapter

> Adapter do integracji z frameworkiem CrewAI.
> **Szacowany czas**: 1-1.5h | **Zadania**: 5.1 - 5.3

---

### [ ] 5.1 Utworzenie Base Adapter

- **Plik(i)**: `agent-orchestrator/backend/app/adapters/base.py`
- **Wymaga**: 2.3
- **Opis**: Utwórz abstrakcyjną klasę bazową dla adapterów.

**Zawartość pliku:**
```python
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
```

**Kryteria akceptacji:**
- [ ] Plik `adapters/base.py` istnieje
- [ ] Klasa `BaseAdapter` jest abstrakcyjna (ABC)
- [ ] Modele `AgentConfig` i `TaskResult` są zdefiniowane
- [ ] Metody abstrakcyjne: `name`, `create_agent`, `execute_task`

---

### [ ] 5.2 Utworzenie CrewAI Adapter

- **Plik(i)**: `agent-orchestrator/backend/app/adapters/crewai_adapter.py`
- **Wymaga**: 5.1
- **Opis**: Utwórz adapter dla frameworka CrewAI.

**Zawartość pliku:**
```python
"""CrewAI framework adapter."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Any
import time

from crewai import Agent, Task, Crew, Process
from langchain.llms.base import LLM

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

    def _create_sync_llm_wrapper(self, tier: str) -> LLM:
        """Create synchronous LLM wrapper for CrewAI.

        CrewAI uses LangChain's sync LLM interface, so we need
        to wrap our async router in a sync wrapper.
        """
        router = self.llm

        class SyncRouterLLM(LLM):
            """Sync wrapper around async LLM router."""

            @property
            def _llm_type(self) -> str:
                return "router"

            def _call(self, prompt: str, stop: Optional[list[str]] = None, **kwargs) -> str:
                """Sync call that runs async code in new event loop."""
                loop = asyncio.new_event_loop()
                try:
                    if tier == "planning":
                        return loop.run_until_complete(router.planning_call(prompt))
                    else:
                        return loop.run_until_complete(router.execution_call(prompt))
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
```

**Kryteria akceptacji:**
- [ ] Plik `adapters/crewai_adapter.py` istnieje
- [ ] Klasa `CrewAIAdapter` dziedziczy po `BaseAdapter`
- [ ] `_create_sync_llm_wrapper()` tworzy sync wrapper dla async routera
- [ ] `execute_task()` używa ThreadPoolExecutor dla sync CrewAI
- [ ] Obsługa błędów zwraca `TaskResult` z `success=False`

---

### [ ] 5.3 Eksport Adapters modułu

- **Plik(i)**: `agent-orchestrator/backend/app/adapters/__init__.py`
- **Wymaga**: 5.1, 5.2
- **Opis**: Wyeksportuj adaptery.

**Zawartość pliku:**
```python
"""AI agent framework adapters package."""

from app.adapters.base import BaseAdapter, AgentConfig, TaskResult
from app.adapters.crewai_adapter import CrewAIAdapter

__all__ = [
    "BaseAdapter",
    "AgentConfig",
    "TaskResult",
    "CrewAIAdapter",
]
```

**Kryteria akceptacji:**
- [ ] Plik `adapters/__init__.py` eksportuje wszystkie klasy

---

## FAZA 6: Frontend

> Aplikacja React z komponentami TaskInput, TaskBoard, CostDashboard.
> **Szacowany czas**: 2-3h | **Zadania**: 6.1 - 6.8

---

### [ ] 6.1 Utworzenie TypeScript Types

- **Plik(i)**: `agent-orchestrator/frontend/src/types/index.ts`
- **Wymaga**: 0.4
- **Opis**: Utwórz typy TypeScript odpowiadające schematom backend.

**Zawartość pliku:**
```typescript
// Task types
export type TaskStatus = 'pending' | 'decomposing' | 'ready' | 'in_progress' | 'completed' | 'failed';
export type SubTaskComplexity = 'simple' | 'medium' | 'complex';
export type ExecutionStatus = 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface SubTask {
  id: string;
  title: string;
  description: string;
  complexity: SubTaskComplexity;
  status: TaskStatus;
  dependencies: string[];
  acceptance_criteria: string[];
}

export interface Task {
  id: string;
  description: string;
  status: TaskStatus;
  subtasks: SubTask[];
  created_at: string;
  updated_at: string | null;
}

export interface TaskDecomposition {
  original_task: string;
  subtasks: Omit<SubTask, 'id' | 'status'>[];
  execution_order: string[][];
  estimated_cost_usd: number;
}

// Execution types
export interface ExecutionLogEntry {
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
  agent?: string;
}

export interface Execution {
  id: string;
  task_id: string;
  status: ExecutionStatus;
  output: string | null;
  logs: ExecutionLogEntry[];
  started_at: string | null;
  completed_at: string | null;
  execution_time_seconds: number | null;
}

export interface ExecutionProgress {
  execution_id: string;
  type: 'status' | 'log' | 'complete' | 'error' | 'connected';
  data: Record<string, unknown>;
}

// Cost types
export interface CostSummary {
  today_cloud_usd: number;
  today_tokens_input: number;
  today_tokens_output: number;
  budget_limit_usd: number;
  budget_remaining_usd: number;
  budget_percent_used: number;
}

// API types
export interface ApiError {
  detail: string | { error: string; message: string };
}
```

**Kryteria akceptacji:**
- [ ] Plik `types/index.ts` istnieje
- [ ] Typy `Task`, `SubTask`, `TaskDecomposition` są zdefiniowane
- [ ] Typy `Execution`, `ExecutionProgress` są zdefiniowane
- [ ] Typ `CostSummary` jest zdefiniowany

---

### [ ] 6.2 Utworzenie API Client (Axios)

- **Plik(i)**: `agent-orchestrator/frontend/src/api.ts`
- **Wymaga**: 6.1
- **Opis**: Utwórz klienta Axios do komunikacji z backendem.

**Zawartość pliku:**
```typescript
import axios, { AxiosInstance } from 'axios';
import type { Task, TaskDecomposition, Execution, CostSummary } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_KEY = import.meta.env.VITE_API_KEY || 'dev-api-key-change-in-production';

// Create axios instance with default config
const api: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
});

// Task endpoints
export const taskApi = {
  decompose: async (description: string): Promise<TaskDecomposition> => {
    const response = await api.post<TaskDecomposition>('/tasks/decompose', { description });
    return response.data;
  },

  create: async (description: string): Promise<Task> => {
    const response = await api.post<Task>('/tasks', { description });
    return response.data;
  },

  get: async (taskId: string): Promise<Task> => {
    const response = await api.get<Task>(`/tasks/${taskId}`);
    return response.data;
  },

  execute: async (taskId: string): Promise<{ execution_id: string }> => {
    const response = await api.post<{ execution_id: string }>(`/tasks/${taskId}/execute`);
    return response.data;
  },
};

// Execution endpoints
export const executionApi = {
  get: async (executionId: string): Promise<Execution> => {
    const response = await api.get<Execution>(`/executions/${executionId}`);
    return response.data;
  },
};

// Cost endpoints
export const costApi = {
  getSummary: async (): Promise<CostSummary> => {
    const response = await api.get<CostSummary>('/costs/summary');
    return response.data;
  },
};

// Health check (no auth required)
export const healthApi = {
  check: async (): Promise<{ status: string; checks: Record<string, boolean> }> => {
    const response = await axios.get(`${API_URL}/health`);
    return response.data;
  },
};

export default api;
```

**Kryteria akceptacji:**
- [ ] Plik `api.ts` istnieje
- [ ] Axios instance z X-API-Key header
- [ ] Funkcje `taskApi.decompose`, `taskApi.create`, `taskApi.execute`
- [ ] Funkcja `costApi.getSummary`

---

### [ ] 6.3 Utworzenie WebSocket Hook

- **Plik(i)**: `agent-orchestrator/frontend/src/hooks/useWebSocket.ts`
- **Wymaga**: 6.1
- **Opis**: Utwórz hook React do obsługi WebSocket dla progress updates.

**Zawartość pliku:**
```typescript
import { useEffect, useRef, useState, useCallback } from 'react';
import type { ExecutionProgress } from '../types';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

interface UseWebSocketOptions {
  executionId: string;
  onProgress?: (progress: ExecutionProgress) => void;
  onError?: (error: Event) => void;
  autoReconnect?: boolean;
}

interface UseWebSocketReturn {
  isConnected: boolean;
  lastMessage: ExecutionProgress | null;
  connect: () => void;
  disconnect: () => void;
}

export function useWebSocket({
  executionId,
  onProgress,
  onError,
  autoReconnect = true,
}: UseWebSocketOptions): UseWebSocketReturn {
  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<ExecutionProgress | null>(null);
  const reconnectTimeoutRef = useRef<number>();

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const ws = new WebSocket(`${WS_URL}/ws/executions/${executionId}`);

    ws.onopen = () => {
      setIsConnected(true);
      console.log(`WebSocket connected for execution ${executionId}`);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as ExecutionProgress;
        setLastMessage(data);
        onProgress?.(data);
      } catch (e) {
        // Handle ping/pong text messages
        if (event.data === 'ping') {
          ws.send('pong');
        }
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log(`WebSocket disconnected for execution ${executionId}`);

      // Auto-reconnect after 3 seconds
      if (autoReconnect) {
        reconnectTimeoutRef.current = window.setTimeout(() => {
          connect();
        }, 3000);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      onError?.(error);
    };

    wsRef.current = ws;
  }, [executionId, onProgress, onError, autoReconnect]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    wsRef.current?.close();
    wsRef.current = null;
  }, []);

  // Connect on mount, disconnect on unmount
  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    connect,
    disconnect,
  };
}
```

**Kryteria akceptacji:**
- [ ] Plik `hooks/useWebSocket.ts` istnieje
- [ ] Hook zwraca `isConnected`, `lastMessage`, `connect`, `disconnect`
- [ ] Auto-reconnect po 3 sekundach
- [ ] Obsługa ping/pong

---

### [ ] 6.4 Utworzenie komponentu TaskInput

- **Plik(i)**: `agent-orchestrator/frontend/src/components/TaskInput.tsx`
- **Wymaga**: 6.2
- **Opis**: Utwórz komponent do wprowadzania zadań.

**Zawartość pliku:**
```typescript
import { useState } from 'react';
import { taskApi } from '../api';
import type { TaskDecomposition } from '../types';

interface TaskInputProps {
  onDecomposed?: (decomposition: TaskDecomposition) => void;
  onError?: (error: string) => void;
}

export function TaskInput({ onDecomposed, onError }: TaskInputProps) {
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!description.trim() || description.length < 10) {
      onError?.('Task description must be at least 10 characters');
      return;
    }

    setIsLoading(true);

    try {
      const decomposition = await taskApi.decompose(description);
      onDecomposed?.(decomposition);
      setDescription('');
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Failed to decompose task';
      onError?.(typeof message === 'string' ? message : message.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="task-input">
      <div className="task-input__field">
        <label htmlFor="task-description">Describe your task:</label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g., Create a REST API endpoint for user authentication with JWT tokens..."
          rows={4}
          disabled={isLoading}
          minLength={10}
          maxLength={5000}
        />
        <span className="task-input__count">{description.length} / 5000</span>
      </div>

      <button
        type="submit"
        disabled={isLoading || description.length < 10}
        className="task-input__submit"
      >
        {isLoading ? 'Decomposing...' : 'Decompose Task'}
      </button>

      {isLoading && (
        <p className="task-input__info">
          Using Claude to analyze and decompose your task...
        </p>
      )}
    </form>
  );
}
```

**Kryteria akceptacji:**
- [ ] Plik `components/TaskInput.tsx` istnieje
- [ ] Textarea z walidacją (min 10, max 5000 znaków)
- [ ] Przycisk "Decompose Task" wywołuje API
- [ ] Loading state podczas dekompozycji
- [ ] Callback `onDecomposed` z wynikiem

---

### [ ] 6.5 Utworzenie komponentu TaskBoard

- **Plik(i)**: `agent-orchestrator/frontend/src/components/TaskBoard.tsx`
- **Wymaga**: 6.1
- **Opis**: Utwórz komponent wyświetlający subtaski w kolumnach (Kanban-style).

**Zawartość pliku:**
```typescript
import type { SubTask, TaskStatus } from '../types';

interface TaskBoardProps {
  subtasks: SubTask[];
  onSubtaskClick?: (subtask: SubTask) => void;
}

const STATUS_COLUMNS: { status: TaskStatus; label: string }[] = [
  { status: 'pending', label: 'Pending' },
  { status: 'in_progress', label: 'In Progress' },
  { status: 'completed', label: 'Completed' },
  { status: 'failed', label: 'Failed' },
];

const COMPLEXITY_COLORS: Record<string, string> = {
  simple: '#4ade80',    // green
  medium: '#fbbf24',    // yellow
  complex: '#f87171',   // red
};

export function TaskBoard({ subtasks, onSubtaskClick }: TaskBoardProps) {
  const getSubtasksByStatus = (status: TaskStatus): SubTask[] => {
    return subtasks.filter((st) => st.status === status);
  };

  return (
    <div className="task-board">
      {STATUS_COLUMNS.map(({ status, label }) => (
        <div key={status} className="task-board__column">
          <h3 className="task-board__column-header">
            {label}
            <span className="task-board__count">
              {getSubtasksByStatus(status).length}
            </span>
          </h3>

          <div className="task-board__cards">
            {getSubtasksByStatus(status).map((subtask) => (
              <div
                key={subtask.id}
                className="task-board__card"
                onClick={() => onSubtaskClick?.(subtask)}
              >
                <div className="task-board__card-header">
                  <span
                    className="task-board__complexity"
                    style={{ backgroundColor: COMPLEXITY_COLORS[subtask.complexity] }}
                  >
                    {subtask.complexity}
                  </span>
                </div>

                <h4 className="task-board__card-title">{subtask.title}</h4>

                <p className="task-board__card-description">
                  {subtask.description.slice(0, 100)}
                  {subtask.description.length > 100 && '...'}
                </p>

                {subtask.dependencies.length > 0 && (
                  <div className="task-board__dependencies">
                    Depends on: {subtask.dependencies.length} task(s)
                  </div>
                )}
              </div>
            ))}

            {getSubtasksByStatus(status).length === 0 && (
              <p className="task-board__empty">No tasks</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
```

**Kryteria akceptacji:**
- [ ] Plik `components/TaskBoard.tsx` istnieje
- [ ] 4 kolumny: Pending, In Progress, Completed, Failed
- [ ] Karty z tytułem, opisem, complexity badge
- [ ] Kolor complexity: green/yellow/red

---

### [ ] 6.6 Utworzenie komponentu CostDashboard

- **Plik(i)**: `agent-orchestrator/frontend/src/components/CostDashboard.tsx`
- **Wymaga**: 6.2
- **Opis**: Utwórz komponent wyświetlający koszty LLM.

**Zawartość pliku:**
```typescript
import { useEffect, useState } from 'react';
import { costApi } from '../api';
import type { CostSummary } from '../types';

interface CostDashboardProps {
  refreshInterval?: number; // ms, default 30000
}

export function CostDashboard({ refreshInterval = 30000 }: CostDashboardProps) {
  const [costs, setCosts] = useState<CostSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCosts = async () => {
    try {
      const summary = await costApi.getSummary();
      setCosts(summary);
      setError(null);
    } catch (err: any) {
      setError('Failed to load cost data');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCosts();
    const interval = setInterval(fetchCosts, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  if (isLoading) {
    return <div className="cost-dashboard cost-dashboard--loading">Loading costs...</div>;
  }

  if (error || !costs) {
    return <div className="cost-dashboard cost-dashboard--error">{error}</div>;
  }

  const isOverBudget = costs.budget_percent_used >= 100;
  const isWarning = costs.budget_percent_used >= 80;

  return (
    <div className={`cost-dashboard ${isOverBudget ? 'cost-dashboard--danger' : isWarning ? 'cost-dashboard--warning' : ''}`}>
      <h3 className="cost-dashboard__title">Today's Usage</h3>

      <div className="cost-dashboard__grid">
        <div className="cost-dashboard__stat">
          <span className="cost-dashboard__label">Cloud LLM Cost</span>
          <span className="cost-dashboard__value">${costs.today_cloud_usd.toFixed(4)}</span>
        </div>

        <div className="cost-dashboard__stat">
          <span className="cost-dashboard__label">Budget Remaining</span>
          <span className="cost-dashboard__value">${costs.budget_remaining_usd.toFixed(2)}</span>
        </div>

        <div className="cost-dashboard__stat">
          <span className="cost-dashboard__label">Input Tokens</span>
          <span className="cost-dashboard__value">{costs.today_tokens_input.toLocaleString()}</span>
        </div>

        <div className="cost-dashboard__stat">
          <span className="cost-dashboard__label">Output Tokens</span>
          <span className="cost-dashboard__value">{costs.today_tokens_output.toLocaleString()}</span>
        </div>
      </div>

      <div className="cost-dashboard__progress">
        <div className="cost-dashboard__progress-bar">
          <div
            className="cost-dashboard__progress-fill"
            style={{ width: `${Math.min(costs.budget_percent_used, 100)}%` }}
          />
        </div>
        <span className="cost-dashboard__progress-label">
          {costs.budget_percent_used.toFixed(1)}% of ${costs.budget_limit_usd} daily budget
        </span>
      </div>

      {isOverBudget && (
        <p className="cost-dashboard__alert">
          ⚠️ Daily budget exceeded! Cloud LLM calls are blocked.
        </p>
      )}
    </div>
  );
}
```

**Kryteria akceptacji:**
- [ ] Plik `components/CostDashboard.tsx` istnieje
- [ ] Wyświetla: koszt, pozostały budżet, tokeny
- [ ] Pasek postępu z % wykorzystania
- [ ] Alert gdy budżet przekroczony (>= 100%)
- [ ] Ostrzeżenie gdy > 80%

---

### [ ] 6.7 Utworzenie głównego App.tsx

- **Plik(i)**: `agent-orchestrator/frontend/src/App.tsx`
- **Wymaga**: 6.4, 6.5, 6.6
- **Opis**: Utwórz główny komponent aplikacji.

**Zawartość pliku:**
```typescript
import { useState } from 'react';
import { TaskInput } from './components/TaskInput';
import { TaskBoard } from './components/TaskBoard';
import { CostDashboard } from './components/CostDashboard';
import type { TaskDecomposition, SubTask } from './types';
import './App.css';

function App() {
  const [decomposition, setDecomposition] = useState<TaskDecomposition | null>(null);
  const [subtasks, setSubtasks] = useState<SubTask[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleDecomposed = (result: TaskDecomposition) => {
    setDecomposition(result);
    // Convert decomposition subtasks to SubTask with id and status
    const subtasksWithIds: SubTask[] = result.subtasks.map((st, index) => ({
      ...st,
      id: `subtask-${index}`,
      status: 'pending' as const,
    }));
    setSubtasks(subtasksWithIds);
    setError(null);
  };

  const handleError = (message: string) => {
    setError(message);
  };

  const handleSubtaskClick = (subtask: SubTask) => {
    console.log('Subtask clicked:', subtask);
    // TODO: Show subtask details modal
  };

  return (
    <div className="app">
      <header className="app__header">
        <h1>Agent Orchestrator</h1>
        <p>AI-powered task decomposition and execution</p>
      </header>

      <div className="app__sidebar">
        <CostDashboard />
      </div>

      <main className="app__main">
        <section className="app__input-section">
          <TaskInput onDecomposed={handleDecomposed} onError={handleError} />

          {error && (
            <div className="app__error">
              {error}
              <button onClick={() => setError(null)}>×</button>
            </div>
          )}
        </section>

        {decomposition && (
          <section className="app__decomposition">
            <h2>Task Decomposition</h2>
            <p>
              <strong>Original:</strong> {decomposition.original_task}
            </p>
            <p>
              <strong>Estimated cost:</strong> ${decomposition.estimated_cost_usd.toFixed(4)}
            </p>
            <p>
              <strong>Subtasks:</strong> {decomposition.subtasks.length}
            </p>
          </section>
        )}

        {subtasks.length > 0 && (
          <section className="app__board-section">
            <h2>Subtasks</h2>
            <TaskBoard subtasks={subtasks} onSubtaskClick={handleSubtaskClick} />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
```

**Kryteria akceptacji:**
- [ ] Plik `App.tsx` istnieje
- [ ] Layout: header, sidebar (costs), main (input + board)
- [ ] State: decomposition, subtasks, error
- [ ] Integracja TaskInput, TaskBoard, CostDashboard

---

### [ ] 6.8 Utworzenie plików konfiguracyjnych frontendu

- **Plik(i)**:
  - `agent-orchestrator/frontend/src/main.tsx`
  - `agent-orchestrator/frontend/src/App.css`
  - `agent-orchestrator/frontend/vite.config.ts`
  - `agent-orchestrator/frontend/tsconfig.json`
  - `agent-orchestrator/frontend/index.html`
- **Wymaga**: 0.4
- **Opis**: Utwórz pliki konfiguracyjne i entry point.

**Zawartość `main.tsx`:**
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**Zawartość `vite.config.ts`:**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
});
```

**Zawartość `tsconfig.json`:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**Zawartość `index.html`:**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Agent Orchestrator</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Kryteria akceptacji:**
- [ ] Plik `main.tsx` renderuje `<App />`
- [ ] Plik `vite.config.ts` konfiguruje proxy do backendu
- [ ] Plik `tsconfig.json` z konfiguracją TypeScript
- [ ] Plik `index.html` z `<div id="root">`

---

## FAZA 7: Docker i Integracja

> Docker Compose, Alembic migrations, integracja end-to-end.
> **Szacowany czas**: 1-1.5h | **Zadania**: 7.1 - 7.5

---

### [ ] 7.1 Utworzenie docker-compose.yml

- **Plik(i)**: `agent-orchestrator/docker-compose.yml`
- **Wymaga**: 0.1
- **Opis**: Utwórz Docker Compose dla lokalnego środowiska.

**Zawartość pliku:**
```yaml
version: '3.8'

services:
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/orchestrator
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - EXECUTION_LLM_URL=${EXECUTION_LLM_URL:-http://host.docker.internal:11434}
      - EXECUTION_LLM_MODEL=${EXECUTION_LLM_MODEL:-qwen2.5-coder:32b}
      - API_KEY=${API_KEY:-dev-api-key-change-in-production}
      - DAILY_BUDGET_USD=${DAILY_BUDGET_USD:-5.0}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
      - POSTGRES_DB=orchestrator
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000
      - VITE_API_KEY=${API_KEY:-dev-api-key-change-in-production}
    depends_on:
      - api
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host

volumes:
  postgres_data:
  redis_data:
```

**Kryteria akceptacji:**
- [ ] Plik `docker-compose.yml` istnieje
- [ ] Serwisy: api, db, redis, frontend
- [ ] Healthcheck dla PostgreSQL
- [ ] Volumes dla danych

---

### [ ] 7.2 Utworzenie Dockerfile dla backendu

- **Plik(i)**: `agent-orchestrator/backend/Dockerfile`
- **Wymaga**: 0.3
- **Opis**: Utwórz Dockerfile dla aplikacji FastAPI.

**Zawartość pliku:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Kryteria akceptacji:**
- [ ] Plik `backend/Dockerfile` istnieje
- [ ] Base image: python:3.11-slim
- [ ] Non-root user dla bezpieczeństwa
- [ ] Expose port 8000

---

### [ ] 7.3 Utworzenie Dockerfile dla frontendu

- **Plik(i)**: `agent-orchestrator/frontend/Dockerfile`
- **Wymaga**: 0.4
- **Opis**: Utwórz Dockerfile dla aplikacji React.

**Zawartość pliku:**
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host"]
```

**Kryteria akceptacji:**
- [ ] Plik `frontend/Dockerfile` istnieje
- [ ] Base image: node:20-alpine
- [ ] Expose port 3000

---

### [ ] 7.4 Konfiguracja Alembic

- **Plik(i)**:
  - `agent-orchestrator/backend/alembic.ini`
  - `agent-orchestrator/backend/alembic/env.py`
- **Wymaga**: 1.6, 1.7
- **Opis**: Skonfiguruj Alembic dla migracji bazy danych.

**Zawartość `alembic.ini`:**
```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

**Zawartość `alembic/env.py`:**
```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from app.config import get_settings
from app.models import Base

config = context.config
settings = get_settings()

# Set sqlalchemy.url from settings
config.set_main_option("sqlalchemy.url", settings.database_url.replace("+asyncpg", ""))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**Kryteria akceptacji:**
- [ ] Plik `alembic.ini` istnieje
- [ ] Plik `alembic/env.py` używa async engine
- [ ] `target_metadata = Base.metadata`

---

### [ ] 7.5 Utworzenie pierwszej migracji

- **Plik(i)**: `agent-orchestrator/backend/alembic/versions/001_initial.py`
- **Wymaga**: 7.4
- **Opis**: Utwórz pierwszą migrację tworzącą tabele.

**Zawartość pliku:**
```python
"""Initial migration - create tasks, subtasks, executions tables.

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'decomposing', 'ready', 'in_progress', 'completed', 'failed', name='taskstatus'), nullable=False),
        sa.Column('decomposition_data', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    # SubTasks table
    op.create_table(
        'subtasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('complexity', sa.Enum('simple', 'medium', 'complex', name='subtaskcomplexity'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'decomposing', 'ready', 'in_progress', 'completed', 'failed', name='taskstatus'), nullable=False),
        sa.Column('dependencies', postgresql.JSON(), default=[]),
        sa.Column('acceptance_criteria', postgresql.JSON(), default=[]),
        sa.Column('order_index', sa.Integer(), default=0),
    )

    # Executions table
    op.create_table(
        'executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id'), nullable=False),
        sa.Column('status', sa.Enum('queued', 'running', 'completed', 'failed', 'cancelled', name='executionstatus'), nullable=False),
        sa.Column('output', sa.Text(), nullable=True),
        sa.Column('logs', postgresql.JSON(), default=[]),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('execution_time_seconds', sa.Float(), nullable=True),
        sa.Column('adapter_name', sa.String(50), default='crewai'),
        sa.Column('cost_usd', sa.Float(), default=0.0),
    )

    # Indexes
    op.create_index('ix_tasks_status', 'tasks', ['status'])
    op.create_index('ix_subtasks_task_id', 'subtasks', ['task_id'])
    op.create_index('ix_executions_task_id', 'executions', ['task_id'])


def downgrade() -> None:
    op.drop_index('ix_executions_task_id')
    op.drop_index('ix_subtasks_task_id')
    op.drop_index('ix_tasks_status')
    op.drop_table('executions')
    op.drop_table('subtasks')
    op.drop_table('tasks')
    op.execute('DROP TYPE IF EXISTS executionstatus')
    op.execute('DROP TYPE IF EXISTS subtaskcomplexity')
    op.execute('DROP TYPE IF EXISTS taskstatus')
```

**Kryteria akceptacji:**
- [ ] Plik migracji istnieje w `alembic/versions/`
- [ ] Tworzy tabele: tasks, subtasks, executions
- [ ] Tworzy indeksy
- [ ] Funkcja `downgrade()` usuwa wszystko

---

## FAZA 8: Testy i Demo

> Testy jednostkowe, integracyjne, scenariusze demo.
> **Szacowany czas**: 2-3h | **Zadania**: 8.1 - 8.5

---

### [ ] 8.1 Utworzenie conftest.py dla pytest

- **Plik(i)**: `agent-orchestrator/backend/tests/conftest.py`
- **Wymaga**: 0.3
- **Opis**: Utwórz fixtures dla testów pytest.

**Zawartość pliku:**
```python
"""Pytest configuration and fixtures."""

import asyncio
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.models import Base
from app.dependencies import get_db


# Test database URL (SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    session_factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def api_headers():
    """Headers for API requests."""
    return {
        "X-API-Key": "dev-api-key-change-in-production",
        "Content-Type": "application/json",
    }
```

**Kryteria akceptacji:**
- [ ] Plik `tests/conftest.py` istnieje
- [ ] Fixture `client` dla AsyncClient
- [ ] Fixture `db_session` dla testowej bazy
- [ ] Fixture `api_headers` z X-API-Key

---

### [ ] 8.2 Testy Task Decomposer

- **Plik(i)**: `agent-orchestrator/backend/tests/test_task_decomposer.py`
- **Wymaga**: 8.1, 3.2
- **Opis**: Utwórz testy dla TaskDecomposer (z mockiem LLM).

**Zawartość pliku:**
```python
"""Tests for TaskDecomposer."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.task_decomposer import TaskDecomposer
from app.schemas.task import TaskDecomposition, SubTaskBase, SubTaskComplexity


@pytest.fixture
def mock_llm_router():
    """Create mock LLM router."""
    router = MagicMock()
    router.planning_call = AsyncMock()
    return router


@pytest.fixture
def decomposer(mock_llm_router):
    """Create TaskDecomposer with mock router."""
    return TaskDecomposer(mock_llm_router)


@pytest.mark.asyncio
async def test_decompose_returns_task_decomposition(decomposer, mock_llm_router):
    """Test that decompose returns TaskDecomposition."""
    # Arrange
    expected = TaskDecomposition(
        original_task="Create a REST API",
        subtasks=[
            SubTaskBase(
                title="Setup FastAPI",
                description="Create main.py with FastAPI app",
                complexity=SubTaskComplexity.SIMPLE,
                dependencies=[],
                acceptance_criteria=["FastAPI app runs"],
            ),
        ],
        execution_order=[["Setup FastAPI"]],
        estimated_cost_usd=0.05,
    )
    mock_llm_router.planning_call.return_value = expected

    # Act
    result = await decomposer.decompose("Create a REST API")

    # Assert
    assert isinstance(result, TaskDecomposition)
    assert result.original_task == "Create a REST API"
    assert len(result.subtasks) == 1
    mock_llm_router.planning_call.assert_called_once()


@pytest.mark.asyncio
async def test_validate_decomposition_valid(decomposer):
    """Test validation passes for valid decomposition."""
    decomposition = TaskDecomposition(
        original_task="Test task",
        subtasks=[
            SubTaskBase(
                title="Step 1",
                description="Do step 1",
                complexity=SubTaskComplexity.SIMPLE,
                dependencies=[],
                acceptance_criteria=["Done"],
            ),
        ],
        execution_order=[["Step 1"]],
        estimated_cost_usd=0.01,
    )

    errors = await decomposer.validate_decomposition(decomposition)
    assert errors == []


@pytest.mark.asyncio
async def test_validate_decomposition_no_subtasks(decomposer):
    """Test validation fails when no subtasks."""
    decomposition = TaskDecomposition(
        original_task="Test",
        subtasks=[],
        execution_order=[],
        estimated_cost_usd=0.0,
    )

    errors = await decomposer.validate_decomposition(decomposition)
    assert "no subtasks" in errors[0].lower()
```

**Kryteria akceptacji:**
- [ ] Plik `tests/test_task_decomposer.py` istnieje
- [ ] Test `test_decompose_returns_task_decomposition`
- [ ] Test `test_validate_decomposition_valid`
- [ ] Użycie `AsyncMock` dla LLM router

---

### [ ] 8.3 Testy API Endpoints

- **Plik(i)**: `agent-orchestrator/backend/tests/test_api_tasks.py`
- **Wymaga**: 8.1, 4.2
- **Opis**: Utwórz testy integracyjne dla API.

**Zawartość pliku:**
```python
"""Integration tests for Tasks API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health endpoint returns 200."""
    response = await client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, api_headers):
    """Test creating a new task."""
    response = await client.post(
        "/api/v1/tasks",
        json={"description": "Test task description for testing"},
        headers=api_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Test task description for testing"
    assert data["status"] == "pending"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_task_without_api_key(client: AsyncClient):
    """Test creating task without API key returns 401."""
    response = await client.post(
        "/api/v1/tasks",
        json={"description": "Test task description for testing"},
    )

    assert response.status_code == 422  # Missing header


@pytest.mark.asyncio
async def test_create_task_short_description(client: AsyncClient, api_headers):
    """Test creating task with too short description."""
    response = await client.post(
        "/api/v1/tasks",
        json={"description": "Short"},
        headers=api_headers,
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_task_not_found(client: AsyncClient, api_headers):
    """Test getting non-existent task returns 404."""
    response = await client.get(
        "/api/v1/tasks/00000000-0000-0000-0000-000000000000",
        headers=api_headers,
    )

    assert response.status_code == 404
```

**Kryteria akceptacji:**
- [ ] Plik `tests/test_api_tasks.py` istnieje
- [ ] Test health endpoint
- [ ] Test create task (success + errors)
- [ ] Test get task not found

---

### [ ] 8.4 Testy Cost Tracker

- **Plik(i)**: `agent-orchestrator/backend/tests/test_cost_tracker.py`
- **Wymaga**: 8.1, 3.1
- **Opis**: Utwórz testy dla CostTracker.

**Zawartość pliku:**
```python
"""Tests for CostTracker."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.cost_tracker import CostTracker, PRICING
from app.llm.router import LLMTier


@pytest.fixture
def mock_redis():
    """Create mock Redis client."""
    redis = MagicMock()
    redis.get = AsyncMock(return_value=None)
    redis.pipeline = MagicMock()

    pipe = MagicMock()
    pipe.incrbyfloat = MagicMock(return_value=pipe)
    pipe.incrby = MagicMock(return_value=pipe)
    pipe.expire = MagicMock(return_value=pipe)
    pipe.execute = AsyncMock(return_value=[])

    redis.pipeline.return_value = pipe
    return redis


@pytest.fixture
def cost_tracker(mock_redis):
    """Create CostTracker with mock Redis."""
    return CostTracker(redis=mock_redis, daily_budget=5.0)


@pytest.mark.asyncio
async def test_get_summary_empty(cost_tracker):
    """Test get_summary with no usage."""
    summary = await cost_tracker.get_summary()

    assert summary.today_cloud_usd == 0.0
    assert summary.budget_remaining_usd == 5.0
    assert summary.budget_percent_used == 0.0


@pytest.mark.asyncio
async def test_is_budget_exceeded_false(cost_tracker):
    """Test budget not exceeded when under limit."""
    exceeded = await cost_tracker.is_budget_exceeded()
    assert exceeded is False


@pytest.mark.asyncio
async def test_is_budget_exceeded_true(cost_tracker, mock_redis):
    """Test budget exceeded when over limit."""
    mock_redis.get = AsyncMock(return_value="5.50")  # Over $5 budget

    exceeded = await cost_tracker.is_budget_exceeded()
    assert exceeded is True


@pytest.mark.asyncio
async def test_log_planning_tier(cost_tracker, mock_redis):
    """Test logging planning tier usage."""
    await cost_tracker.log(
        tier=LLMTier.PLANNING,
        provider="anthropic",
        input_tokens=1000,
        output_tokens=500,
    )

    # Verify pipeline was called
    mock_redis.pipeline.assert_called_once()


def test_pricing_constants():
    """Test pricing constants are set."""
    assert "anthropic" in PRICING
    assert PRICING["anthropic"]["input"] > 0
    assert PRICING["anthropic"]["output"] > 0
    assert PRICING["ollama"]["input"] == 0
    assert PRICING["ollama"]["output"] == 0
```

**Kryteria akceptacji:**
- [ ] Plik `tests/test_cost_tracker.py` istnieje
- [ ] Test get_summary
- [ ] Test is_budget_exceeded (true/false)
- [ ] Test log z mock Redis

---

### [ ] 8.5 Scenariusze Demo

- **Plik(i)**: `agent-orchestrator/DEMO_SCENARIOS.md`
- **Wymaga**: Wszystkie poprzednie fazy
- **Opis**: Utwórz dokumentację scenariuszy demo.

**Zawartość pliku:**
```markdown
# Agent Orchestrator - Scenariusze Demo

## Przygotowanie

1. Uruchom infrastrukturę:
   ```bash
   make docker-up
   ```

2. Uruchom migracje:
   ```bash
   make migrate
   ```

3. Uruchom backend:
   ```bash
   make dev-backend
   ```

4. Uruchom frontend:
   ```bash
   make dev-frontend
   ```

5. (Opcjonalnie) Uruchom Ollama z modelem:
   ```bash
   ollama run qwen2.5-coder:32b
   ```

---

## Scenariusz 1: Prosty REST API

**Zadanie:** "Create a FastAPI endpoint that returns a list of users from a PostgreSQL database"

**Oczekiwany wynik:**
- 4-6 subtasków
- Complexity: 2 simple, 2-3 medium, 0-1 complex
- Koszt decompose: < $0.05

**Kroki:**
1. Otwórz http://localhost:3000
2. Wpisz zadanie w polu tekstowym
3. Kliknij "Decompose Task"
4. Sprawdź czy subtaski pojawiły się na TaskBoard

---

## Scenariusz 2: Refactoring kodu

**Zadanie:** "Refactor the authentication module to use JWT tokens instead of session cookies, maintaining backward compatibility"

**Oczekiwany wynik:**
- 5-8 subtasków
- Zawiera subtask "complex" dla architektury
- Execution order z zależnościami

---

## Scenariusz 3: Bug fix

**Zadanie:** "Fix the race condition in the order processing service that causes duplicate orders when users double-click the submit button"

**Oczekiwany wynik:**
- 3-5 subtasków
- Zawiera: analiza, implementacja, testy

---

## Scenariusz 4: Nowa funkcjonalność

**Zadanie:** "Add a dark mode toggle to the React application with system preference detection and local storage persistence"

**Oczekiwany wynik:**
- 4-6 subtasków
- Równoległe subtaski dla CSS i logiki

---

## Scenariusz 5: Test budżetu

**Zadanie:** Wykonaj 50+ dekompozycji aby sprawdzić czy budżet się wyczerpie.

**Oczekiwany wynik:**
- CostDashboard pokazuje rosnące koszty
- Po przekroczeniu $5: błąd 402 Payment Required

---

## Weryfikacja sukcesu POC

- [ ] `/tasks/decompose` zwraca JSON w <10s
- [ ] WebSocket pokazuje "connected"
- [ ] CostDashboard aktualizuje się co 30s
- [ ] Wszystkie 5 scenariuszy działa
- [ ] Koszt pojedynczej dekompozycji < $0.10
```

**Kryteria akceptacji:**
- [ ] Plik `DEMO_SCENARIOS.md` istnieje
- [ ] 5 scenariuszy demo opisanych
- [ ] Checklist weryfikacji sukcesu POC

---

## Podsumowanie

| Faza | Zadania | Opis |
|------|---------|------|
| 0 | 0.1-0.8 | Setup projektu (struktura, config) |
| 1 | 1.1-1.8 | Backend Core (modele, schematy, FastAPI) |
| 2 | 2.1-2.4 | LLM Integration (router, providery) |
| 3 | 3.1-3.4 | Core Logic (decomposer, cost tracker, engine) |
| 4 | 4.1-4.6 | API Endpoints (routes, WebSocket) |
| 5 | 5.1-5.3 | CrewAI Adapter |
| 6 | 6.1-6.8 | Frontend (React components) |
| 7 | 7.1-7.5 | Docker i Integracja |
| 8 | 8.1-8.5 | Testy i Demo |

**Łącznie: 42 zadania**

---

*Dokument wygenerowany automatycznie. Data: 2026-01-08*

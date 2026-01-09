# Architektura Agent Orchestrator

> **Dokument referencyjny:** Ten dokument opisuje wysokopoziomową architekturę systemu.
> Szczegółowy plan implementacji: [PLAN_DEVELOPMENT.md](../PLAN_DEVELOPMENT.md)

---

## Przegląd Systemu

Agent Orchestrator to meta-framework łączący funkcje z LangGraph, CrewAI, AutoGen i Agency Swarm z hybrydową architekturą LLM.

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND                                   │
│                     React + TypeScript + Vite                        │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐            │
│  │ TaskInput   │  │ TaskBoard   │  │ CostDashboard    │            │
│  └─────────────┘  └─────────────┘  └──────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                               │
                         REST API / WebSocket
                               │
┌─────────────────────────────────────────────────────────────────────┐
│                            BACKEND                                   │
│                        FastAPI + Python 3.11                         │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                         API Layer                               │ │
│  │   /tasks/decompose  │  /tasks/{id}  │  /costs  │  /ws/tasks   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                               │                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                         Core Layer                              │ │
│  │   TaskDecomposer  │  ExecutionEngine  │  CostTracker          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                               │                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                      LLM Router Layer                           │ │
│  │        ┌──────────────┬──────────────────────┐                 │ │
│  │        │ Planning Tier │ Execution Tier       │                 │ │
│  │        │ (Cloud API)   │ (Self-hosted)        │                 │ │
│  │        │ Claude/GPT-4  │ Ollama/Qwen          │                 │ │
│  │        └──────────────┴──────────────────────┘                 │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                               │                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                     Adapters Layer                              │ │
│  │   CrewAI Adapter  │  (planowane: LangGraph, AutoGen)          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                               │                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                      Data Layer                                 │ │
│  │           SQLAlchemy Models  │  Redis Cache                    │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼───────┐      ┌───────▼───────┐      ┌──────▼──────┐
│  PostgreSQL   │      │     Redis     │      │   Ollama    │
│  (Persistence)│      │    (Cache)    │      │  (Local LLM)│
└───────────────┘      └───────────────┘      └─────────────┘
```

---

## Warstwy Systemu

### 1. Frontend Layer

**Technologie:** React 18, TypeScript, Vite, TanStack Query, Zustand

**Komponenty:**

| Komponent | Lokalizacja | Odpowiedzialność |
|-----------|-------------|------------------|
| `TaskInput` | `frontend/src/components/TaskInput.tsx` | Formularz do wprowadzania zadań |
| `TaskBoard` | `frontend/src/components/TaskBoard.tsx` | Wyświetlanie zadań i subtasków |
| `CostDashboard` | `frontend/src/components/CostDashboard.tsx` | Dashboard kosztów LLM |

**Komunikacja:**
- REST API dla operacji CRUD
- WebSocket dla real-time updates (status, logi)

---

### 2. API Layer

**Technologie:** FastAPI, Pydantic v2

**Endpointy:**

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/api/v1/tasks/decompose` | POST | Dekompozycja zadania na subtaski |
| `/api/v1/tasks/{id}` | GET | Pobierz szczegóły zadania |
| `/api/v1/tasks/{id}/execute` | POST | Uruchom wykonanie zadania |
| `/api/v1/executions/{id}` | GET | Pobierz status wykonania |
| `/api/v1/costs/summary` | GET | Podsumowanie kosztów |
| `/ws/tasks/{id}` | WebSocket | Real-time updates |
| `/health` | GET | Health check |

Szczegóły: [docs/API.md](API.md)

---

### 3. Core Layer

**Kluczowe komponenty:**

#### TaskDecomposer
```
Lokalizacja: backend/app/core/task_decomposer.py

Odpowiedzialność:
├── Przyjmuje opis zadania (string)
├── Wysyła do Planning LLM (Claude)
├── Parsuje strukturalną odpowiedź (JSON)
└── Zwraca TaskDecomposition z listą SubTask
```

#### ExecutionEngine
```
Lokalizacja: backend/app/core/execution_engine.py

Odpowiedzialność:
├── Przyjmuje Task + Adapter (CrewAI)
├── Iteruje po subtaskach w kolejności wykonania
├── Deleguje wykonanie do adaptera
├── Emituje progress updates (WebSocket)
└── Zwraca wynik wykonania
```

#### CostTracker
```
Lokalizacja: backend/app/core/cost_tracker.py

Odpowiedzialność:
├── Loguje użycie tokenów (input/output)
├── Kalkuluje koszty (per provider)
├── Przechowuje w Redis (dzienne agregaty)
├── Sprawdza limity budżetowe
└── Generuje raporty kosztów
```

---

### 4. LLM Router Layer

**Architektura hybrydowa:**

```
                    ┌─────────────────────────┐
                    │       LLM Router        │
                    │  backend/app/llm/router.py
                    └───────────┬─────────────┘
                                │
           ┌────────────────────┼────────────────────┐
           │                                         │
  ┌────────▼────────┐                     ┌─────────▼─────────┐
  │  PLANNING TIER  │                     │  EXECUTION TIER   │
  │   (Cloud API)   │                     │  (Self-hosted)    │
  ├─────────────────┤                     ├───────────────────┤
  │ Claude 3.5      │                     │ Ollama (local)    │
  │ GPT-4o          │                     │ OpenRouter API    │
  ├─────────────────┤                     ├───────────────────┤
  │ ~5% wywołań     │                     │ ~95% wywołań      │
  │ $3-15/1M tokens │                     │ $0 (self-hosted)  │
  └─────────────────┘                     └───────────────────┘

  Zastosowanie:                           Zastosowanie:
  - Dekompozycja zadań                    - Implementacja kodu
  - Architektura                          - Testy
  - Code review                           - Refactoring
  - Decyzje strategiczne                  - Dokumentacja
```

**Providers:**

| Provider | Plik | Tier |
|----------|------|------|
| Anthropic | `backend/app/llm/providers/anthropic.py` | Planning |
| OpenAI-compatible | `backend/app/llm/providers/openai_compatible.py` | Execution |

---

### 5. Adapters Layer

**Wzorzec:** Strategy Pattern

```python
# backend/app/adapters/base.py
class BaseAdapter(ABC):
    @abstractmethod
    async def create_agent(self, config: AgentConfig) -> Any: ...

    @abstractmethod
    async def execute_task(self, agent, task_description, context) -> TaskResult: ...
```

**Dostępne adaptery:**

| Adapter | Status | Plik |
|---------|--------|------|
| CrewAI | ✅ Zaimplementowany | `backend/app/adapters/crewai_adapter.py` |
| LangGraph | 📋 Planowany | - |
| AutoGen | 📋 Planowany | - |
| Agency Swarm | 📋 Planowany | - |

---

### 6. Data Layer

**Modele SQLAlchemy:**

```
Task (backend/app/models/task.py)
├── id: UUID (PK)
├── description: String
├── status: Enum (pending, decomposing, ready, executing, completed, failed)
├── decomposition_result: JSON
├── estimated_cost_usd: Float
├── created_at: DateTime
└── subtasks: Relationship → SubTask[]

SubTask (backend/app/models/task.py)
├── id: UUID (PK)
├── task_id: UUID (FK → Task)
├── title: String
├── description: String
├── complexity: Enum (simple, medium, complex)
├── dependencies: JSON
├── acceptance_criteria: JSON
├── order_index: Integer
└── status: Enum

Execution (backend/app/models/execution.py)
├── id: UUID (PK)
├── task_id: UUID (FK → Task)
├── status: Enum (pending, running, completed, failed)
├── started_at: DateTime
├── completed_at: DateTime
├── logs: JSON
└── result: JSON
```

**Redis Cache:**

| Klucz | Typ | TTL | Opis |
|-------|-----|-----|------|
| `cost:{date}:cloud` | Float | 24h | Dzienny koszt cloud LLM |
| `tokens:{date}:input` | Int | 24h | Dzienne tokeny input |
| `tokens:{date}:output` | Int | 24h | Dzienne tokeny output |
| `task:{id}:status` | String | 1h | Cache statusu zadania |

---

## Flow Dekompozycji Zadania

```
┌──────────────┐     ┌─────────────┐     ┌──────────────────┐
│   Frontend   │────▶│   API       │────▶│ TaskDecomposer   │
│  TaskInput   │     │ POST /tasks │     │                  │
└──────────────┘     │ /decompose  │     └────────┬─────────┘
                     └─────────────┘              │
                                                  │
                     ┌─────────────┐              │
                     │  LLMRouter  │◀─────────────┘
                     │ planning_call
                     └──────┬──────┘
                            │
                     ┌──────▼──────┐
                     │   Claude    │
                     │   (Cloud)   │
                     └──────┬──────┘
                            │
                     ┌──────▼──────┐
                     │ Structured  │
                     │   Output    │
                     │   (JSON)    │
                     └──────┬──────┘
                            │
                     ┌──────▼──────┐     ┌──────────────┐
                     │  Database   │────▶│   Response   │
                     │  Save Task  │     │ TaskResponse │
                     └─────────────┘     └──────────────┘
```

---

## Flow Wykonania Zadania

```
┌──────────────┐     ┌─────────────┐     ┌──────────────────┐
│   Frontend   │────▶│   API       │────▶│ ExecutionEngine  │
│  TaskBoard   │     │ POST /tasks │     │                  │
└──────────────┘     │ /{id}/execute     └────────┬─────────┘
      ▲              └─────────────┘              │
      │                                           │
      │              ┌─────────────┐              │
      │              │ WebSocket   │◀─────────────┤ emit progress
      │              │ /ws/tasks   │              │
      │              └──────┬──────┘              │
      │                     │                     │
      └─────────────────────┘              ┌──────▼──────┐
        real-time updates                  │ CrewAI      │
                                          │ Adapter     │
                                          └──────┬──────┘
                                                 │
                                          ┌──────▼──────┐
                                          │   Ollama    │
                                          │ (Execution) │
                                          └─────────────┘
```

---

## Bezpieczeństwo

### Autentykacja

```
┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Request    │────▶│ X-API-Key   │────▶│  Validate    │
│              │     │   Header    │     │  API Key     │
└──────────────┘     └─────────────┘     └──────────────┘
```

### Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| `POST /tasks/decompose` | 10 | 1 minuta |
| Pozostałe | 100 | 1 minuta |

### CORS

Konfigurowane przez `CORS_ORIGINS` w `.env`:
```bash
CORS_ORIGINS='["https://yourdomain.com","http://localhost:3000"]'
```

---

## Skalowanie

### Obecne (POC)

```
┌─────────────────────────────────────┐
│           docker-compose            │
│  ┌─────────┐ ┌──────┐ ┌──────────┐ │
│  │   API   │ │  DB  │ │  Redis   │ │
│  │  (1x)   │ │ (1x) │ │   (1x)   │ │
│  └─────────┘ └──────┘ └──────────┘ │
└─────────────────────────────────────┘
```

### Planowane (Produkcja)

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
└────────────────────────┬────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
┌───▼───┐           ┌────▼───┐          ┌────▼───┐
│  API  │           │  API   │          │  API   │
│ (n=3) │           │ (n=3)  │          │ (n=3)  │
└───────┘           └────────┘          └────────┘
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼───┐     ┌─────▼────┐    ┌─────▼────┐
    │ PG     │     │  Redis   │    │  Ollama  │
    │ (HA)   │     │ Cluster  │    │  (GPU)   │
    └────────┘     └──────────┘    └──────────┘
```

---

## Ważne Decyzje Architekturalne

| Decyzja | Uzasadnienie | Alternatywy |
|---------|--------------|-------------|
| Hybrydowy LLM | Minimalizacja kosztów przy zachowaniu jakości | Tylko cloud, tylko local |
| CrewAI jako pierwszy adapter | Dojrzałość, dokumentacja, aktywna społeczność | LangGraph, AutoGen |
| PostgreSQL | Solidność, JSON support, znajomość | MongoDB, SQLite |
| Redis | Szybkość, pub/sub dla WebSocket | In-memory, RabbitMQ |
| FastAPI | Async, automatyczna dokumentacja, typing | Flask, Django |
| Pydantic v2 | Walidacja, structured output z LLM | Marshmallow |

---

## Powiązane dokumenty

- [Pełny plan implementacji](../PLAN_DEVELOPMENT.md)
- [Mapa kodu](CODEBASE.md)
- [Dokumentacja API](API.md)

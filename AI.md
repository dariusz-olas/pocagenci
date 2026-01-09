# Agent Orchestrator - Przewodnik dla Asystentów AI

> **Dla:** Claude Code, Cursor IDE, GitHub Copilot, i innych asystentów AI
> **Wersja:** 0.1.0 (POC)
> **Ostatnia aktualizacja:** 2026-01-09

---

## Szybki Start dla AI

### Czym jest ten projekt?

**Agent Orchestrator** to meta-framework do orkiestracji agentów AI z hybrydową architekturą LLM:
- **Planning Tier** (Cloud API) - Claude/GPT-4 do planowania i dekompozycji zadań
- **Execution Tier** (Self-hosted) - Ollama/Qwen do implementacji

### Kluczowe technologie

| Warstwa | Technologia |
|---------|-------------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy, Alembic, Redis |
| Frontend | React 18, TypeScript, Vite, TanStack Query |
| Baza danych | PostgreSQL 16 |
| Konteneryzacja | Docker, Docker Compose |
| Agenci | CrewAI (POC), planowane: LangGraph, AutoGen |

---

## Dokumentacja - Spis Treści

| Dokument | Opis | Kiedy używać |
|----------|------|--------------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architektura systemu, diagramy, flow | Zrozumienie struktury projektu |
| [docs/CODEBASE.md](docs/CODEBASE.md) | Mapa kodu, ważne pliki, konwencje | Nawigacja po kodzie |
| [docs/API.md](docs/API.md) | Dokumentacja REST API i WebSocket | Praca z endpointami |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Setup, komendy, workflow developmentu | Uruchamianie i rozwijanie |
| [docs/TESTING.md](docs/TESTING.md) | Strategia testów, uruchamianie | Pisanie i uruchamianie testów |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Wytyczne dla kontrybutorów | Przed tworzeniem PR |

### Dokumenty referencyjne (szczegółowe)

| Dokument | Opis |
|----------|------|
| [PLAN_DEVELOPMENT.md](PLAN_DEVELOPMENT.md) | Pełny plan architekturalny POC |
| [PRODUCTION_READINESS.md](PRODUCTION_READINESS.md) | Ocena gotowości produkcyjnej |
| [TASKS.md](TASKS.md) | Szczegółowa lista zadań implementacyjnych |
| [agent-orchestrator/README.md](agent-orchestrator/README.md) | Quick start guide |
| [agent-orchestrator/SETUP.md](agent-orchestrator/SETUP.md) | Konfiguracja środowiska |
| [agent-orchestrator/DEMO_SCENARIOS.md](agent-orchestrator/DEMO_SCENARIOS.md) | Scenariusze demo do testowania |

---

## Struktura Projektu

```
pocagenci/
├── AI.md                          # TEN PLIK - start dla AI
├── docs/                          # Dokumentacja tematyczna
│   ├── ARCHITECTURE.md
│   ├── CODEBASE.md
│   ├── API.md
│   ├── DEVELOPMENT.md
│   └── TESTING.md
├── CONTRIBUTING.md                # Wytyczne dla kontrybutorów
├── PLAN_DEVELOPMENT.md            # Plan architekturalny
├── PRODUCTION_READINESS.md        # Ocena gotowości
├── TASKS.md                       # Lista zadań
│
└── agent-orchestrator/            # Główny kod aplikacji
    ├── README.md
    ├── SETUP.md
    ├── DEMO_SCENARIOS.md
    ├── docker-compose.yml         # Development
    ├── docker-compose.prod.yml    # Production
    ├── Makefile
    │
    ├── backend/                   # FastAPI backend
    │   ├── app/
    │   │   ├── main.py           # Entry point
    │   │   ├── config.py         # Konfiguracja
    │   │   ├── dependencies.py   # Dependency Injection
    │   │   ├── api/routes/       # REST endpoints
    │   │   ├── api/websockets/   # WebSocket handlers
    │   │   ├── core/             # Biznes logika
    │   │   ├── llm/              # LLM routing i providers
    │   │   ├── adapters/         # Adaptery frameworków (CrewAI)
    │   │   ├── models/           # SQLAlchemy models
    │   │   └── schemas/          # Pydantic schemas
    │   ├── tests/
    │   └── alembic/              # Migracje DB
    │
    └── frontend/                  # React frontend
        └── src/
            ├── App.tsx
            ├── api.ts            # API client
            ├── components/       # UI components
            ├── hooks/            # React hooks
            └── types/            # TypeScript types
```

---

## Zasady dla Asystentów AI

### Czego NIE robić

1. **Nie usuwaj komentarzy TODO** - są mapowane do TASKS.md i PRODUCTION_READINESS.md
2. **Nie zmieniaj struktury folderów** bez dyskusji
3. **Nie modyfikuj `alembic/versions/`** bez migracji
4. **Nie commituj sekretów** - sprawdź .env.example zamiast .env
5. **Nie usuwaj testów** nawet jeśli są czerwone
6. **Nie dodawaj nowych zależności** bez uzasadnienia w PR

### Czego OCZEKUJEMY

1. **Pisz testy** dla każdej nowej funkcjonalności
2. **Używaj typów** - TypeScript w frontend, Pydantic w backend
3. **Stosuj konwencje** opisane w docs/CODEBASE.md
4. **Aktualizuj dokumentację** gdy zmieniasz API/schemat
5. **Sprawdzaj PRODUCTION_READINESS.md** przed implementacją - może to już jest zrobione

### Priorytetyzacja zadań

Przed implementacją sprawdź:
1. **PRODUCTION_READINESS.md** - sekcja 2 "KRYTYCZNE BRAKI"
2. **TASKS.md** - status poszczególnych tasków
3. **GitHub Issues** - może jest już zgłoszone

---

## Komendy do uruchomienia

```bash
# Setup
cd agent-orchestrator
cp backend/.env.example backend/.env
# Edytuj .env i dodaj ANTHROPIC_API_KEY

# Development
make install          # Instalacja zależności
make docker-up        # Start PostgreSQL + Redis
make migrate          # Migracje bazy
make backend          # Start backend (http://localhost:8000)
make frontend         # Start frontend (http://localhost:3000)

# Testy
make test             # Wszystkie testy backend
make test-cov         # Testy z coverage

# Linting
make lint             # Sprawdzenie kodu
make format           # Formatowanie
```

---

## Najważniejsze pliki (TOP 10)

| Plik | Opis | Edytuj gdy... |
|------|------|---------------|
| `backend/app/main.py` | Entry point FastAPI | Zmieniasz middleware, CORS |
| `backend/app/config.py` | Konfiguracja aplikacji | Dodajesz zmienne środowiskowe |
| `backend/app/core/task_decomposer.py` | Dekompozycja zadań | Modyfikujesz prompt LLM |
| `backend/app/llm/router.py` | Routing między LLM | Zmieniasz strategię routingu |
| `backend/app/api/routes/tasks.py` | REST API dla zadań | Dodajesz/modyfikujesz endpointy |
| `backend/app/schemas/task.py` | Schematy Pydantic | Zmieniasz strukturę danych |
| `frontend/src/api.ts` | Klient API | Dodajesz wywołania API |
| `frontend/src/App.tsx` | Główny komponent | Zmieniasz layout/routing |
| `docker-compose.yml` | Dev environment | Dodajesz usługi |
| `backend/pyproject.toml` | Zależności Python | Dodajesz biblioteki |

---

## Aktualny Status i Priorytety

### Status: 🟡 POC Gotowe

| Obszar | Status | Szczegóły |
|--------|--------|-----------|
| Struktura projektu | ✅ 100% | Kompletna |
| Backend API | 🟡 75% | Brak background execution |
| Frontend | 🟡 70% | Brak pełnej integracji WebSocket |
| Testy | 🔴 30% | Tylko 13 testów |
| Bezpieczeństwo | 🔴 25% | Wymaga rate limiting, CORS config |

### Priorytety implementacji

1. **KRYTYCZNE** (przed demo):
   - Background task execution - `backend/app/api/routes/tasks.py:141`
   - Subtasks loading - `backend/app/api/routes/tasks.py:98`
   - WebSocket integration z ExecutionEngine

2. **WYSOKIE** (przed staging):
   - Rate limiting
   - CORS configuration
   - Usunięcie domyślnego API key

3. **ŚREDNIE** (przed produkcją):
   - Testy integracyjne
   - Production Dockerfile
   - Monitoring

Szczegóły w: [PRODUCTION_READINESS.md](PRODUCTION_READINESS.md)

---

## Kontakt i Wsparcie

- **Dokumentacja techniczna:** [PLAN_DEVELOPMENT.md](PLAN_DEVELOPMENT.md)
- **Znane problemy:** [PRODUCTION_READINESS.md](PRODUCTION_READINESS.md)
- **Lista zadań:** [TASKS.md](TASKS.md)

---

*Ten dokument jest punktem startowym dla każdego asystenta AI pracującego z projektem. Zawsze zaczynaj od przeczytania tego pliku przed rozpoczęciem pracy.*

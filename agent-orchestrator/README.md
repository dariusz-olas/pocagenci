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

# Agent Orchestrator

Meta-framework łączący funkcje LangGraph, CrewAI, AutoGen i Agency Swarm z hybrydową architekturą LLM.

## Quick Start

### Wymagania
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Ollama (opcjonalnie, dla lokalnego LLM)

### Instalacja

#### Linux/Mac (Makefile)
```bash
# Sklonuj repo
git clone <repo-url>
cd agent-orchestrator

# Skopiuj zmienne środowiskowe
cp backend/.env.example backend/.env
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

#### Windows ARM64 (PowerShell)
```powershell
# Sklonuj repo
git clone <repo-url>
cd agent-orchestrator

# Wygeneruj API key
.\generate-api-key.ps1

# Utwórz backend\.env z wymaganymi kluczami
# (Skopiuj wygenerowany API_KEY i dodaj ANTHROPIC_API_KEY)

# Zainstaluj zależności
.\setup-windows.ps1 install

# Uruchom infrastrukturę
.\setup-windows.ps1 docker-up

# Uruchom migracje
.\setup-windows.ps1 migrate

# Uruchom backend (Terminal 1)
.\setup-windows.ps1 backend

# Uruchom frontend (Terminal 2)
.\setup-windows.ps1 frontend
```

**📚 Więcej informacji:**
- [Szybki Start Windows](QUICK_START_WINDOWS.md)
- [Szczegółowy Przewodnik Windows ARM64](SETUP_WINDOWS_ARM64.md)
- [Komendy PowerShell](POWERSHELL_COMMANDS.md)

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

## Dokumentacja

- [Setup Guide](SETUP.md) - Konfiguracja środowiska
- [Windows ARM64 Setup](SETUP_WINDOWS_ARM64.md) - Szczegółowy przewodnik dla Windows
- [Quick Start Windows](QUICK_START_WINDOWS.md) - Szybki start (5 minut)
- [Verification Checklist](VERIFICATION_CHECKLIST.md) - Checklista weryfikacji
- [Troubleshooting Docker](TROUBLESHOOTING_DOCKER.md) - Rozwiązywanie problemów z Docker
- [Migration Setup](backend/MIGRATION_SETUP.md) - Instrukcje migracji bazy danych
- [Demo Scenarios](DEMO_SCENARIOS.md) - Scenariusze testowe

## Licencja

MIT

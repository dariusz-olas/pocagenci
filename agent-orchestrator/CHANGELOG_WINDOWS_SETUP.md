# Changelog - Windows ARM64 Setup (2026-01-09)

## 🎯 Cel
Przygotowanie projektu do uruchomienia na Windows ARM64 z pełną dokumentacją i narzędziami pomocniczymi.

---

## ✅ Naprawione Problemy

### 1. Problem z pyproject.toml (hatchling)
**Problem:** Hatchling nie mógł określić, które pliki dołączyć do pakietu podczas instalacji.
```
ValueError: Unable to determine which files to ship inside the wheel
```

**Rozwiązanie:**
- Dodano konfigurację `[tool.hatch.build.targets.wheel]` z `packages = ["app"]` w `pyproject.toml`

**Plik:** `backend/pyproject.toml`

---

### 2. Problem z podwójnym `/v1` w execution_llm_url
**Problem:** Jeśli użytkownik ustawił `EXECUTION_LLM_URL=https://openrouter.ai/api/v1`, powstawało `https://openrouter.ai/api/v1/v1`.

**Rozwiązanie:**
- Dodano logikę sprawdzającą czy URL już kończy się na `/v1` przed dodaniem
- Automatyczna zamiana `@db:` na `@localhost:` dla migracji z hosta

**Plik:** `backend/app/dependencies.py`

---

### 3. Problem z migracjami bazy danych
**Problem:** 
- Brak modułu `psycopg2` (Alembic wymaga synchronicznego sterownika)
- Alembic używał async engine, a psycopg2 jest synchroniczny
- DATABASE_URL używał `db` (nazwa kontenera) zamiast `localhost` dla migracji z hosta

**Rozwiązanie:**
- Dodano `psycopg2-binary>=2.9.0` do zależności
- Zmieniono `alembic/env.py` na synchroniczny engine (`engine_from_config` zamiast `async_engine_from_config`)
- Automatyczna zamiana `+asyncpg` na `+psycopg2` i `@db:` na `@localhost:` w `alembic/env.py`

**Pliki:**
- `backend/pyproject.toml`
- `backend/alembic/env.py`
- `backend/MIGRATION_SETUP.md` (nowy dokument)

---

### 4. Problem z brakującym modułem langchain
**Problem:** 
- CrewAI wymaga langchain, ale nie był w zależnościach
- Import `from langchain.llms.base import LLM` nie działał w nowszych wersjach LangChain

**Rozwiązanie:**
- Dodano `langchain>=1.0.0` i `langchain-core>=1.0.0` do zależności
- Zmieniono import z `langchain.llms.base.LLM` na `langchain_core.language_models.base.BaseLanguageModel`
- Zaktualizowano implementację `SyncRouterLLM` w `CrewAIAdapter` z metodą `_generate()` wymaganą przez `BaseLanguageModel`

**Pliki:**
- `backend/pyproject.toml`
- `backend/app/adapters/crewai_adapter.py`

---

### 5. Problem z Docker Compose na Windows ARM64
**Problem:**
- Skrypt nie sprawdzał czy Docker Desktop jest uruchomiony
- Pokazywał sukces mimo błędów
- Ostrzeżenie o przestarzałym `version: '3.8'`

**Rozwiązanie:**
- Dodano sprawdzanie statusu Docker przed uruchomieniem
- Lepsze komunikaty błędów
- Usunięto `version: '3.8'` z `docker-compose.yml`

**Pliki:**
- `agent-orchestrator/setup-windows.ps1`
- `agent-orchestrator/docker-compose.yml`
- `agent-orchestrator/TROUBLESHOOTING_DOCKER.md` (nowy dokument)

---

## 📝 Nowe Dokumenty

### 1. SETUP_WINDOWS_ARM64.md
Szczegółowy przewodnik uruchomienia na Windows ARM64 z 3 opcjami:
- Opcja 1: Uruchomienie natywne (zalecane dla testów)
- Opcja 2: Docker Compose (pełne środowisko)
- Opcja 3: Hybrydowe (infrastruktura w Docker, aplikacje natywnie)

### 2. QUICK_START_WINDOWS.md
Szybki start (5 minut) dla Windows ARM64.

### 3. setup-windows.ps1
PowerShell skrypt jako alternatywa dla Makefile na Windows:
- `install` - Instalacja zależności
- `docker-up` - Uruchom Docker
- `migrate` - Migracje bazy
- `backend` - Uruchom backend
- `frontend` - Uruchom frontend
- `test`, `lint`, `clean`

### 4. generate-api-key.ps1
Generator bezpiecznego API key (32+ znaków) dla Windows.

### 5. POWERSHELL_COMMANDS.md
Przewodnik po komendach PowerShell dla projektu.

### 6. VERIFICATION_CHECKLIST.md
Szczegółowa checklista weryfikacji całego procesu uruchomienia.

### 7. TROUBLESHOOTING_DOCKER.md
Rozwiązywanie problemów z Docker na Windows ARM64.

### 8. MIGRATION_SETUP.md
Instrukcje dotyczące migracji bazy danych.

---

## 🔧 Ulepszenia

### Konfiguracja
- Ulepszona dokumentacja `anthropic_api_key` w `config.py`
- Automatyczna zamiana URL dla migracji (db → localhost)

### Skrypty
- Automatyczna instalacja brakujących zależności (psycopg2-binary, langchain)
- Lepsze komunikaty błędów
- Sprawdzanie statusu Docker przed uruchomieniem

### Dokumentacja
- Dodano sekcję Windows ARM64 do głównych dokumentów
- Przykłady komend PowerShell
- Rozwiązywanie problemów

---

## 📊 Statystyki Zmian

- **Naprawionych problemów:** 5
- **Nowych dokumentów:** 8
- **Zmodyfikowanych plików:** 6
- **Nowych skryptów:** 2

---

## 🎓 Wnioski

### Dla Windows ARM64:
1. **Docker Desktop** wymaga WSL2 i może sprawiać problemy - zalecana opcja hybrydowa
2. **Makefile** nie działa natywnie - użyj `setup-windows.ps1`
3. **Ollama** może nie być dostępne - użyj OpenRouter jako alternatywy
4. **Migracje** wymagają synchronicznego sterownika (psycopg2) i `localhost` zamiast `db`

### Dla Development:
1. **LangChain** zmienił API - użyj `langchain_core.language_models.base.BaseLanguageModel`
2. **CrewAI** wymaga langchain jako zależności
3. **Alembic** wymaga synchronicznego engine dla migracji

### Dla Dokumentacji:
1. Zawsze uwzględniaj różnice między systemami operacyjnymi
2. Dodawaj przykłady dla różnych platform (Linux/Mac/Windows)
3. Twórz skrypty pomocnicze dla każdej platformy

---

## 🚀 Następne Kroki

1. ✅ Projekt działa na Windows ARM64
2. ⏭️ Przetestować na innych platformach (Linux, Mac)
3. ⏭️ Dodać CI/CD dla Windows ARM64
4. ⏭️ Zaktualizować główny README z informacjami o Windows

---

*Data: 2026-01-09*
*Autor: AI Assistant (Claude)*


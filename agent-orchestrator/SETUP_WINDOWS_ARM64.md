# Plan Uruchomienia - Windows ARM64

## 📋 Przegląd

Ten dokument zawiera szczegółowy plan uruchomienia projektu **Agent Orchestrator** na systemie Windows ARM64. Zawiera zarówno instrukcje dla uruchomienia natywnego (bez Docker), jak i z użyciem Docker Desktop.

---

## 🎯 Opcje Uruchomienia

### Opcja 1: Uruchomienie natywne (Zalecane dla testów)
- ✅ Szybsze uruchomienie
- ✅ Łatwiejsze debugowanie
- ✅ Mniejsze zużycie zasobów
- ⚠️ Wymaga lokalnej instalacji PostgreSQL i Redis

### Opcja 2: Docker Compose (Zalecane dla produkcji)
- ✅ Izolowane środowisko
- ✅ Łatwa replikacja
- ✅ Zgodne z dokumentacją projektu
- ⚠️ Wymaga Docker Desktop dla Windows ARM64

### Opcja 3: Hybrydowe (Infrastruktura w Docker, aplikacje natywnie)
- ✅ Najlepsze z obu światów
- ✅ Szybki development
- ✅ Spójne środowisko bazy danych

---

## 🔧 Wymagania Wstępne

### Wymagane (dla wszystkich opcji)
- **Python 3.11+** - [Pobierz dla ARM64](https://www.python.org/downloads/)
- **Node.js 18+** - [Pobierz dla ARM64](https://nodejs.org/)
- **Git** - [Pobierz](https://git-scm.com/download/win)

### Opcjonalne (w zależności od wybranej opcji)
- **Docker Desktop** - [Pobierz dla Windows ARM64](https://www.docker.com/products/docker-desktop/)
- **PostgreSQL 16** (jeśli natywnie) - [Pobierz](https://www.postgresql.org/download/windows/)
- **Redis** (jeśli natywnie) - [Pobierz](https://github.com/microsoftarchive/redis/releases) lub użyj Docker

### Klucze API (WYMAGANE)
- **ANTHROPIC_API_KEY** - [Zdobądź tutaj](https://console.anthropic.com/)
- **API_KEY** - wygeneruj lokalnie (min. 32 znaki)

---

## 🚀 Opcja 1: Uruchomienie Natywne (Zalecane)

### Krok 1: Przygotowanie środowiska

```powershell
# Przejdź do katalogu projektu
cd C:\pocagenci\pocagenci\agent-orchestrator

# Sprawdź wersje
python --version  # Powinno być 3.11+
node --version    # Powinno być 18+
```

### Krok 2: Konfiguracja zmiennych środowiskowych

```powershell
# Skopiuj szablon .env
Copy-Item backend\.env.example backend\.env

# Edytuj backend\.env i ustaw:
# - API_KEY (wygeneruj: użyj skryptu generate-api-key.ps1)
# - ANTHROPIC_API_KEY (z console.anthropic.com)
```

**Wygeneruj API_KEY:**
```powershell
# Użyj PowerShell
$apiKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "API_KEY=$apiKey"
```

### Krok 3: Instalacja zależności

```powershell
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# Frontend
cd ..\frontend
npm install
```

### Krok 4: Uruchomienie infrastruktury (Docker lub natywnie)

#### 4a. Infrastruktura w Docker (Zalecane)

```powershell
# Wróć do głównego katalogu
cd C:\pocagenci\pocagenci\agent-orchestrator

# Uruchom tylko PostgreSQL i Redis
docker-compose up -d db redis

# Sprawdź status
docker-compose ps
```

#### 4b. Infrastruktura natywnie (Alternatywa)

Jeśli masz PostgreSQL i Redis zainstalowane lokalnie:

```powershell
# Uruchom PostgreSQL (jeśli jako usługa Windows)
# Sprawdź czy działa na porcie 5432

# Uruchom Redis (jeśli jako usługa Windows)
# Sprawdź czy działa na porcie 6379
```

### Krok 5: Migracje bazy danych

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```

### Krok 6: Uruchomienie aplikacji

**Terminal 1 - Backend:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

### Krok 7: Weryfikacja

- ✅ Backend: http://localhost:8000/health
- ✅ Frontend: http://localhost:3000
- ✅ API Docs: http://localhost:8000/docs

---

## 🐳 Opcja 2: Docker Compose (Pełne środowisko)

### Krok 1: Przygotowanie

```powershell
cd C:\pocagenci\pocagenci\agent-orchestrator

# Ustaw zmienne środowiskowe
$env:API_KEY = "twoj-wygenerowany-klucz-min-32-znaki"
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

### Krok 2: Uruchomienie

```powershell
# Uruchom wszystkie usługi
docker-compose up --build

# Lub w tle
docker-compose up -d --build
```

### Krok 3: Migracje

```powershell
# Wykonaj migracje w kontenerze
docker-compose exec api alembic upgrade head
```

### Krok 4: Weryfikacja

- ✅ Backend: http://localhost:8000/health
- ✅ Frontend: http://localhost:3000
- ✅ API Docs: http://localhost:8000/docs

### Krok 5: Logi

```powershell
# Wszystkie logi
docker-compose logs -f

# Tylko backend
docker-compose logs -f api
```

---

## 🔄 Opcja 3: Hybrydowe (Zalecane dla Development)

### Infrastruktura w Docker, aplikacje natywnie

```powershell
# 1. Uruchom tylko infrastrukturę
docker-compose up -d db redis

# 2. Uruchom backend natywnie (Terminal 1)
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000

# 3. Uruchom frontend natywnie (Terminal 2)
cd frontend
npm run dev
```

**Zalety:**
- Szybkie hot-reload
- Łatwe debugowanie
- Spójna baza danych

---

## 🧪 Testowanie Funkcjonalności

### 1. Test Health Check

```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Lub curl
curl http://localhost:8000/health
```

### 2. Test Decompose Task

```powershell
$headers = @{
    "X-API-Key" = "twoj-api-key"
    "Content-Type" = "application/json"
}

$body = @{
    description = "Create a FastAPI endpoint that returns a list of users"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/decompose" `
    -Method POST `
    -Headers $headers `
    -Body $body
```

### 3. Test Frontend

1. Otwórz http://localhost:3000
2. Wpisz zadanie w polu tekstowym
3. Kliknij "Decompose Task"
4. Sprawdź czy subtaski pojawiły się na TaskBoard

---

## 🔧 Rozwiązywanie Problemów

### Problem: Port już zajęty

```powershell
# Znajdź proces na porcie 8000
netstat -ano | findstr :8000

# Zabij proces (zastąp <PID> rzeczywistym ID)
taskkill /PID <PID> /F
```

### Problem: Docker nie działa na ARM64

1. Sprawdź czy Docker Desktop jest zainstalowany dla ARM64
2. Sprawdź czy WSL2 jest włączony (wymagane dla Docker Desktop)
3. Użyj opcji natywnej (Opcja 1)

### Problem: Błąd połączenia z bazą danych

```powershell
# Sprawdź czy PostgreSQL działa
docker-compose ps db

# Sprawdź logi
docker-compose logs db

# Test połączenia
docker-compose exec db psql -U postgres -d orchestrator -c "SELECT 1;"
```

### Problem: Błąd importu Python

```powershell
# Upewnij się, że venv jest aktywne
cd backend
.\.venv\Scripts\Activate.ps1

# Reinstalacja zależności
pip install -e ".[dev]"
```

### Problem: Ollama nie działa (Execution LLM)

**Opcja A: Użyj OpenRouter zamiast Ollama**

Edytuj `backend\.env`:
```env
EXECUTION_LLM_URL=https://openrouter.ai/api/v1
EXECUTION_LLM_MODEL=deepseek/deepseek-coder:33b
OPENROUTER_API_KEY=twoj-klucz
```

**Opcja B: Zainstaluj Ollama dla Windows ARM64**

1. Pobierz Ollama dla Windows: https://ollama.ai/download
2. Uruchom: `ollama run qwen2.5-coder:32b`
3. Sprawdź: `curl http://localhost:11434/api/tags`

---

## 📝 Zmienne Środowiskowe

### Wymagane

| Zmienna | Opis | Przykład |
|---------|------|----------|
| `API_KEY` | Klucz API (min 32 znaki) | Wygeneruj lokalnie |
| `ANTHROPIC_API_KEY` | Klucz Anthropic Claude | `sk-ant-api03-...` |
| `DATABASE_URL` | URL bazy PostgreSQL | `postgresql+asyncpg://postgres:postgres@localhost:5432/orchestrator` |
| `REDIS_URL` | URL Redis | `redis://localhost:6379` |

### Opcjonalne

| Zmienna | Domyślna wartość | Opis |
|---------|-----------------|------|
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Lista dozwolonych origins |
| `DAILY_BUDGET_USD` | `5.0` | Dzienny budżet LLM (USD) |
| `EXECUTION_LLM_URL` | `http://localhost:11434` | URL lokalnego LLM (Ollama) |
| `EXECUTION_LLM_MODEL` | `qwen2.5-coder:32b` | Model do wykonania |
| `OPENROUTER_API_KEY` | - | Klucz OpenRouter (alternatywa dla Ollama) |

---

## 🎯 Rekomendowana Ścieżka dla Windows ARM64

**Dla szybkich testów:**
1. Użyj **Opcji 3 (Hybrydowe)**
2. Infrastruktura w Docker (PostgreSQL + Redis)
3. Aplikacje natywnie (szybki hot-reload)
4. OpenRouter zamiast Ollama (łatwiejsze setup)

**Dla pełnego testowania:**
1. Użyj **Opcji 2 (Docker Compose)**
2. Wszystko w kontenerach
3. Zgodne z dokumentacją projektu

---

## 📚 Dodatkowe Zasoby

- [Dokumentacja projektu](README.md)
- [Scenariusze demo](DEMO_SCENARIOS.md)
- [Dokumentacja developmentu](../docs/DEVELOPMENT.md)
- [Dokumentacja API](../docs/API.md)

---

## ✅ Checklist Uruchomienia

- [ ] Python 3.11+ zainstalowany
- [ ] Node.js 18+ zainstalowany
- [ ] Docker Desktop zainstalowany (opcjonalnie)
- [ ] `.env` skonfigurowany z wymaganymi kluczami
- [ ] Zależności zainstalowane (backend i frontend)
- [ ] Infrastruktura uruchomiona (PostgreSQL + Redis)
- [ ] Migracje wykonane
- [ ] Backend działa na http://localhost:8000
- [ ] Frontend działa na http://localhost:3000
- [ ] Health check przechodzi
- [ ] Test decompose task działa

---

*Ostatnia aktualizacja: 2026-01-09*


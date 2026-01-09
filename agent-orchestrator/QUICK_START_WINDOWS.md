# 🚀 Szybki Start - Windows ARM64

## Najszybsza ścieżka uruchomienia (5 minut)

### 1. Przygotowanie

```powershell
# Przejdź do katalogu projektu
cd C:\pocagenci\pocagenci\agent-orchestrator

# Sprawdź czy masz Python i Node.js
python --version  # Powinno być 3.11+
node --version   # Powinno być 18+
```

### 2. Konfiguracja

```powershell
# Utwórz plik .env w backend
cd backend
@"
API_KEY=wygeneruj-klucz-min-32-znaki-tutaj
ANTHROPIC_API_KEY=sk-ant-api03-twoj-klucz-tutaj
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orchestrator
REDIS_URL=redis://localhost:6379
"@ | Out-File -FilePath .env -Encoding utf8

# Wygeneruj API_KEY (32+ znaki)
cd ..
.\generate-api-key.ps1
# Skopiuj wygenerowany klucz do backend\.env
```

### 3. Instalacja

```powershell
# Użyj PowerShell skryptu
.\setup-windows.ps1 install

# LUB ręcznie:
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# Frontend
cd ..\frontend
npm install
```

### 4. Infrastruktura

```powershell
# Uruchom PostgreSQL i Redis w Docker
.\setup-windows.ps1 docker-up

# LUB ręcznie:
docker-compose up -d db redis
```

### 5. Migracje

```powershell
.\setup-windows.ps1 migrate

# LUB ręcznie:
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```

### 6. Uruchomienie

**Terminal 1 - Backend:**
```powershell
.\setup-windows.ps1 backend

# LUB ręcznie:
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
.\setup-windows.ps1 frontend

# LUB ręcznie:
cd frontend
npm run dev
```

### 7. Weryfikacja

- ✅ Backend: http://localhost:8000/health
- ✅ Frontend: http://localhost:3000
- ✅ API Docs: http://localhost:8000/docs

---

## 🎯 Rekomendowana konfiguracja dla Windows ARM64

### Opcja A: Hybrydowe (Najlepsze dla development)

```powershell
# 1. Infrastruktura w Docker
docker-compose up -d db redis

# 2. Backend natywnie (Terminal 1)
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000

# 3. Frontend natywnie (Terminal 2)
cd frontend
npm run dev
```

**Zalety:**
- ✅ Szybki hot-reload
- ✅ Łatwe debugowanie
- ✅ Mniejsze zużycie zasobów

### Opcja B: Pełne Docker (Najlepsze dla testów)

```powershell
# Ustaw zmienne środowiskowe
$env:API_KEY = "twoj-wygenerowany-klucz-min-32-znaki"
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."

# Uruchom wszystko
docker-compose up --build

# Migracje
docker-compose exec api alembic upgrade head
```

**Zalety:**
- ✅ Izolowane środowisko
- ✅ Zgodne z dokumentacją
- ✅ Łatwa replikacja

---

## 🔑 Generowanie API Key

```powershell
# Użyj skryptu
.\generate-api-key.ps1

# LUB ręcznie w PowerShell:
$apiKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "API_KEY=$apiKey"
```

---

## ⚠️ Ważne Uwagi dla Windows ARM64

1. **Docker Desktop** - Upewnij się, że masz wersję dla ARM64
2. **WSL2** - Wymagane dla Docker Desktop (jeśli używasz Docker)
3. **Ollama** - Może nie być dostępne dla Windows ARM64, użyj OpenRouter jako alternatywy:

```env
# W backend\.env
EXECUTION_LLM_URL=https://openrouter.ai/api/v1
EXECUTION_LLM_MODEL=deepseek/deepseek-coder:33b
OPENROUTER_API_KEY=twoj-klucz-openrouter
```

---

## 🧪 Test Funkcjonalności

```powershell
# Test Health Check
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Test Decompose (wymaga API_KEY w headers)
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

---

## 📚 Więcej Informacji

- Szczegółowy przewodnik: [SETUP_WINDOWS_ARM64.md](SETUP_WINDOWS_ARM64.md)
- Scenariusze demo: [DEMO_SCENARIOS.md](DEMO_SCENARIOS.md)
- Dokumentacja API: [../docs/API.md](../docs/API.md)
- Komendy PowerShell: [POWERSHELL_COMMANDS.md](POWERSHELL_COMMANDS.md)

---

## 🆘 Problemy?

### Port zajęty
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Docker nie działa
Użyj opcji hybrydowej - infrastruktura w Docker, aplikacje natywnie.

### Błąd importu Python
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

---

*Gotowe! Projekt powinien działać. Jeśli masz problemy, sprawdź [SETUP_WINDOWS_ARM64.md](SETUP_WINDOWS_ARM64.md) dla szczegółowych instrukcji.*


# PowerShell - Przydatne Komendy dla Windows

## 🔄 Nawigacja po Katalogach

### Przejście do katalogu nadrzędnego
```powershell
# ✅ POPRAWNIE (PowerShell)
cd ..

# ❌ BŁĘDNIE (to jest składnia bash/Linux)
./..
```

### Przejście do konkretnego katalogu
```powershell
# Przejdź do katalogu nadrzędnego, potem do frontend
cd ..\frontend

# Przejdź do backend
cd backend

# Przejdź do głównego katalogu projektu
cd C:\pocagenci\pocagenci\agent-orchestrator
```

### Sprawdzenie aktualnej lokalizacji
```powershell
# Pokaż aktualną ścieżkę
pwd
# LUB
Get-Location

# Pokaż zawartość katalogu
ls
# LUB
Get-ChildItem
```

---

## 🐍 Praca z Python Virtual Environment

### Aktywacja virtual environment
```powershell
# W katalogu backend
cd backend
.\.venv\Scripts\Activate.ps1

# Sprawdź czy jest aktywny (powinno pokazać (.venv) na początku)
python --version
```

### Deaktywacja virtual environment
```powershell
deactivate
```

### Jeśli masz błąd "execution of scripts is disabled"
```powershell
# Uruchom PowerShell jako Administrator i wykonaj:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📦 Instalacja i Zarządzanie Zależnościami

### Backend (Python)
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Frontend (Node.js)
```powershell
cd frontend
npm install
```

---

## 🐳 Docker Komendy

### Uruchomienie kontenerów
```powershell
# W głównym katalogu projektu
docker-compose up -d db redis

# Wszystkie usługi
docker-compose up -d
```

### Sprawdzenie statusu
```powershell
docker-compose ps
```

### Logi
```powershell
docker-compose logs -f api
docker-compose logs -f db
```

### Zatrzymanie
```powershell
docker-compose down
```

---

## 🔧 Uruchomienie Aplikacji

### Backend
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### Frontend
```powershell
cd frontend
npm run dev
```

---

## 🗄️ Migracje Bazy Danych

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```

---

## 🧪 Testy

### Backend testy
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -v
```

---

## 🔑 Generowanie API Key

```powershell
# Użyj skryptu
.\generate-api-key.ps1

# LUB ręcznie
$apiKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "API_KEY=$apiKey"
```

---

## 📝 Praca z Plikami

### Utworzenie pliku .env
```powershell
cd backend
@"
API_KEY=twoj-klucz-tutaj
ANTHROPIC_API_KEY=sk-ant-api03-...
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orchestrator
REDIS_URL=redis://localhost:6379
"@ | Out-File -FilePath .env -Encoding utf8
```

### Sprawdzenie czy plik istnieje
```powershell
Test-Path backend\.env
```

### Wyświetlenie zawartości pliku
```powershell
Get-Content backend\.env
```

---

## 🌐 Testowanie API

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

### Decompose Task
```powershell
$headers = @{
    "X-API-Key" = "twoj-api-key"
    "Content-Type" = "application/json"
}
$body = @{
    description = "Create a REST API endpoint"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/decompose" `
    -Method POST `
    -Headers $headers `
    -Body $body
```

---

## 🔍 Diagnostyka

### Sprawdzenie portów
```powershell
# Znajdź proces na porcie 8000
netstat -ano | findstr :8000

# Zabij proces (zastąp <PID> rzeczywistym ID)
taskkill /PID <PID> /F
```

### Sprawdzenie wersji
```powershell
python --version
node --version
docker --version
git --version
```

---

## ⚠️ Częste Błędy i Rozwiązania

### Błąd: "./.." nie jest rozpoznane
**Problem:** Używasz składni bash w PowerShell
**Rozwiązanie:** Użyj `cd ..` zamiast `./..`

### Błąd: execution of scripts is disabled
**Problem:** PowerShell blokuje wykonywanie skryptów
**Rozwiązanie:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Błąd: nie można znaleźć modułu
**Problem:** Virtual environment nie jest aktywny
**Rozwiązanie:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
```

---

## 💡 Przydatne Skróty

| Komenda | Opis |
|---------|------|
| `cd ..` | Przejdź do katalogu nadrzędnego |
| `cd ~` | Przejdź do katalogu domowego |
| `cd -` | Przejdź do poprzedniego katalogu |
| `ls` | Lista plików (alias dla Get-ChildItem) |
| `pwd` | Pokaż aktualną ścieżkę (alias dla Get-Location) |
| `cls` | Wyczyść konsolę (alias dla Clear-Host) |
| `Ctrl+C` | Przerwij działający proces |

---

*Ten dokument zawiera najczęściej używane komendy PowerShell dla pracy z projektem Agent Orchestrator na Windows.*


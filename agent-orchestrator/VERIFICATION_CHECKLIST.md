# Checklist Weryfikacji Uruchomienia - Windows ARM64

## ✅ Naprawione Problemy

### 1. ✅ Problem z pyproject.toml (hatchling)
**Problem:** Hatchling nie mógł określić, które pliki dołączyć do pakietu.
**Rozwiązanie:** Dodano konfigurację `[tool.hatch.build.targets.wheel]` z `packages = ["app"]`.

### 2. ✅ Problem z podwójnym /v1 w execution_llm_url
**Problem:** Jeśli użytkownik ustawi `EXECUTION_LLM_URL=https://openrouter.ai/api/v1`, to powstawało `https://openrouter.ai/api/v1/v1`.
**Rozwiązanie:** Dodano logikę sprawdzającą czy URL już kończy się na `/v1` przed dodaniem.

### 3. ✅ Ulepszona dokumentacja anthropic_api_key
**Zmiana:** Dodano Field z opisem dla lepszej dokumentacji.

---

## 📋 Checklist Weryfikacji Krok po Kroku

### Krok 1: Przygotowanie Środowiska

- [ ] Python 3.11+ zainstalowany
  ```powershell
  python --version
  ```
  **Oczekiwany wynik:** Python 3.11.x lub wyższy

- [ ] Node.js 18+ zainstalowany
  ```powershell
  node --version
  ```
  **Oczekiwany wynik:** v18.x.x lub wyższy

- [ ] Docker Desktop zainstalowany (opcjonalnie, dla infrastruktury)
  ```powershell
  docker --version
  docker-compose --version
  ```

- [ ] Git zainstalowany
  ```powershell
  git --version
  ```

### Krok 2: Konfiguracja Zmiennych Środowiskowych

- [ ] Plik `backend\.env` utworzony
  ```powershell
  Test-Path backend\.env
  ```
  **Powinno zwrócić:** `True`

- [ ] API_KEY wygenerowany (min 32 znaki)
  ```powershell
  .\generate-api-key.ps1
  ```
  **Sprawdź:** Czy klucz ma minimum 32 znaki

- [ ] ANTHROPIC_API_KEY ustawiony
  ```powershell
  # W backend\.env sprawdź czy jest:
  # ANTHROPIC_API_KEY=sk-ant-api03-...
  ```
  **Uwaga:** Jeśli puste, aplikacja uruchomi się, ale decompose task nie zadziała.

- [ ] DATABASE_URL skonfigurowany
  ```powershell
  # Dla Docker: postgresql+asyncpg://postgres:postgres@localhost:5432/orchestrator
  # Dla natywnego: dostosuj do swojej konfiguracji
  ```

- [ ] REDIS_URL skonfigurowany
  ```powershell
  # Dla Docker: redis://localhost:6379
  # Dla natywnego: dostosuj do swojej konfiguracji
  ```

### Krok 3: Instalacja Zależności

- [ ] Backend zależności zainstalowane
  ```powershell
  cd backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -e ".[dev]"
  ```
  **Sprawdź:** Czy instalacja zakończyła się bez błędów

- [ ] Frontend zależności zainstalowane
  ```powershell
  cd frontend
  npm install
  ```
  **Sprawdź:** Czy instalacja zakończyła się bez błędów (ostrzeżenia są OK)

### Krok 4: Infrastruktura

- [ ] PostgreSQL uruchomiony
  ```powershell
  # Opcja A: Docker
  docker-compose up -d db
  
  # Opcja B: Sprawdź czy działa natywnie
  # (jeśli masz PostgreSQL zainstalowany lokalnie)
  ```
  **Weryfikacja:**
  ```powershell
  docker-compose ps db
  # Powinno pokazać: Up (healthy)
  ```

- [ ] Redis uruchomiony
  ```powershell
  # Opcja A: Docker
  docker-compose up -d redis
  
  # Opcja B: Sprawdź czy działa natywnie
  ```
  **Weryfikacja:**
  ```powershell
  docker-compose ps redis
  # Powinno pokazać: Up
  ```

### Krok 5: Migracje Bazy Danych

- [ ] Migracje wykonane
  ```powershell
  cd backend
  .\.venv\Scripts\Activate.ps1
  alembic upgrade head
  ```
  **Sprawdź:** Czy migracje zakończyły się sukcesem
  **Oczekiwany wynik:** `INFO  [alembic.runtime.migration] Running upgrade -> 001_initial, Initial migration`

- [ ] Tabele utworzone w bazie
  ```powershell
  # Opcjonalnie - sprawdź w bazie:
  docker-compose exec db psql -U postgres -d orchestrator -c "\dt"
  ```
  **Oczekiwane tabele:** `tasks`, `subtasks`, `executions`

### Krok 6: Uruchomienie Backend

- [ ] Backend uruchomiony
  ```powershell
  cd backend
  .\.venv\Scripts\Activate.ps1
  uvicorn app.main:app --reload --port 8000
  ```
  **Sprawdź logi:**
  - Czy nie ma błędów importu
  - Czy widzisz: `Application startup complete`
  - Czy widzisz: `Uvicorn running on http://0.0.0.0:8000`

- [ ] Health check działa
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8000/health"
  ```
  **Oczekiwany wynik:**
  ```json
  {
    "status": "healthy",
    "checks": {
      "database": true,
      "redis": true,
      "llm_planning": true/false,
      "llm_execution": true/false
    }
  }
  ```

- [ ] API Docs dostępne
  ```powershell
  # Otwórz w przeglądarce:
  Start-Process "http://localhost:8000/docs"
  ```
  **Sprawdź:** Czy Swagger UI się ładuje

### Krok 7: Uruchomienie Frontend

- [ ] Frontend uruchomiony
  ```powershell
  cd frontend
  npm run dev
  ```
  **Sprawdź logi:**
  - Czy widzisz: `Local: http://localhost:3000/`
  - Czy nie ma błędów kompilacji

- [ ] Frontend dostępny w przeglądarce
  ```powershell
  Start-Process "http://localhost:3000"
  ```
  **Sprawdź:** Czy strona się ładuje bez błędów w konsoli

### Krok 8: Test Funkcjonalności

- [ ] Test decompose task (wymaga ANTHROPIC_API_KEY)
  ```powershell
  $headers = @{
      "X-API-Key" = "twoj-api-key-z-env"
      "Content-Type" = "application/json"
  }
  $body = @{
      description = "Create a simple REST API endpoint"
  } | ConvertTo-Json
  
  Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/decompose" `
      -Method POST `
      -Headers $headers `
      -Body $body
  ```
  **Oczekiwany wynik:** JSON z `subtasks`, `execution_order`, `estimated_cost_usd`

- [ ] Test przez frontend
  - Otwórz http://localhost:3000
  - Wpisz zadanie w polu tekstowym
  - Kliknij "Decompose Task"
  - **Sprawdź:** Czy subtaski pojawiły się na TaskBoard

- [ ] Test cost summary
  ```powershell
  $headers = @{
      "X-API-Key" = "twoj-api-key-z-env"
  }
  Invoke-RestMethod -Uri "http://localhost:8000/api/v1/costs/summary" `
      -Headers $headers
  ```
  **Oczekiwany wynik:** JSON z `today_cloud`, `budget_remaining`, etc.

### Krok 9: Weryfikacja Integracji

- [ ] WebSocket connection (jeśli zaimplementowane)
  - Sprawdź czy frontend łączy się z WebSocket
  - Sprawdź logi backend dla połączeń WebSocket

- [ ] CORS działa poprawnie
  - Sprawdź czy frontend może wykonywać requesty do backend
  - Sprawdź czy nie ma błędów CORS w konsoli przeglądarki

---

## ⚠️ Znane Problemy i Rozwiązania

### Problem: Błąd "API key must be at least 32 characters"
**Rozwiązanie:** 
```powershell
.\generate-api-key.ps1
# Skopiuj wygenerowany klucz do backend\.env jako API_KEY=...
```

### Problem: Błąd połączenia z bazą danych
**Rozwiązanie:**
```powershell
# Sprawdź czy PostgreSQL działa
docker-compose ps db

# Sprawdź logi
docker-compose logs db

# Sprawdź czy port nie jest zajęty
netstat -ano | findstr :5432
```

### Problem: Błąd połączenia z Redis
**Rozwiązanie:**
```powershell
# Sprawdź czy Redis działa
docker-compose ps redis

# Test połączenia
docker-compose exec redis redis-cli ping
# Powinno zwrócić: PONG
```

### Problem: Anthropic API key pusty - decompose nie działa
**Rozwiązanie:**
- Aplikacja uruchomi się, ale endpoint `/tasks/decompose` zwróci błąd
- Dodaj `ANTHROPIC_API_KEY` do `backend\.env`

### Problem: Execution LLM nie działa (Ollama)
**Rozwiązanie:**
- **Opcja A:** Zainstaluj Ollama dla Windows ARM64
- **Opcja B:** Użyj OpenRouter:
  ```env
  EXECUTION_LLM_URL=https://openrouter.ai/api/v1
  EXECUTION_LLM_MODEL=deepseek/deepseek-coder:33b
  OPENROUTER_API_KEY=twoj-klucz
  ```

### Problem: Port 8000 lub 3000 zajęty
**Rozwiązanie:**
```powershell
# Znajdź proces
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Zabij proces (zastąp <PID>)
taskkill /PID <PID> /F
```

### Problem: Import errors w Python
**Rozwiązanie:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Problem: Docker nie działa na Windows ARM64
**Rozwiązanie:**
- Upewnij się, że masz Docker Desktop dla ARM64
- Sprawdź czy WSL2 jest włączony
- Użyj opcji hybrydowej (infrastruktura w Docker, aplikacje natywnie)

---

## 🎯 Szybka Weryfikacja (5 minut)

Jeśli wszystko działa, powinieneś móc:

1. ✅ Otworzyć http://localhost:8000/health i zobaczyć `{"status": "healthy"}`
2. ✅ Otworzyć http://localhost:8000/docs i zobaczyć Swagger UI
3. ✅ Otworzyć http://localhost:3000 i zobaczyć interfejs frontend
4. ✅ Wykonać decompose task przez API lub frontend (wymaga ANTHROPIC_API_KEY)

---

## 📝 Notatki dla Windows ARM64

1. **Docker Desktop:** Wymaga WSL2, który jest dostępny dla ARM64
2. **Ollama:** Może nie być dostępne dla Windows ARM64 - użyj OpenRouter jako alternatywy
3. **Makefile:** Nie działa natywnie - użyj `setup-windows.ps1` zamiast tego
4. **host.docker.internal:** Działa w Docker Desktop dla Windows

---

*Ostatnia aktualizacja: 2026-01-09*


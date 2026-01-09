# Wytyczne Developmentu - Agent Orchestrator

> **Cel dokumentu:** Setup środowiska, workflow developmentu, komendy.

---

## Wymagania

### Minimalne

- **Python** 3.11+
- **Node.js** 18+
- **Docker** & Docker Compose
- **Git**

### Opcjonalne

- **Ollama** - dla lokalnego LLM (execution tier)
- **Make** - dla wygodnych komend

---

## Szybki Start

### 1. Klonowanie repozytorium

```bash
git clone <repo-url>
cd pocagenci/agent-orchestrator
```

### 2. Konfiguracja środowiska

```bash
# Skopiuj template
cp backend/.env.example backend/.env

# Edytuj .env i dodaj klucze
# WYMAGANE:
# - API_KEY (wygeneruj: openssl rand -hex 32)
# - ANTHROPIC_API_KEY (z console.anthropic.com)
```

### 3. Uruchomienie infrastruktury

```bash
# Uruchom PostgreSQL i Redis
docker-compose up -d db redis

# Sprawdź status
docker-compose ps
```

### 4. Backend

```bash
cd backend

# Utwórz virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalacja zależności
pip install -e ".[dev]"

# Migracje bazy danych
alembic upgrade head

# Uruchom backend
uvicorn app.main:app --reload --port 8000
```

### 5. Frontend

```bash
cd frontend

# Instalacja zależności
npm install

# Uruchom dev server
npm run dev
```

### 6. Weryfikacja

- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## Komendy Makefile

Jeśli masz `make`, możesz użyć wygodnych skrótów:

```bash
# Setup
make install          # Instalacja wszystkich zależności
make docker-up        # Start PostgreSQL + Redis
make docker-down      # Stop kontenerów
make migrate          # Migracje bazy

# Development
make backend          # Start backend (z reload)
make frontend         # Start frontend
make dev              # Start backend + frontend równolegle

# Testy
make test             # Wszystkie testy
make test-cov         # Testy z coverage
make test-watch       # Testy w trybie watch

# Linting & Formatting
make lint             # Sprawdź kod (ruff, mypy)
make format           # Formatuj kod (ruff, prettier)

# Czyszczenie
make clean            # Usuń cache, __pycache__, node_modules
```

---

## Workflow Developmentu

### 1. Tworzenie brancha

```bash
# Format: type/short-description
git checkout -b feature/add-langraph-adapter
git checkout -b fix/websocket-reconnect
git checkout -b refactor/llm-router
```

**Typy branchy:**
- `feature/` - nowa funkcjonalność
- `fix/` - naprawa błędu
- `refactor/` - refaktoryzacja
- `docs/` - dokumentacja
- `test/` - testy

### 2. Praca nad kodem

```bash
# Upewnij się, że testy przechodzą przed commitem
make test

# Sprawdź linting
make lint

# Formatuj kod
make format
```

### 3. Commity

**Format:** `type(scope): description`

```bash
git commit -m "feat(api): add pagination to tasks endpoint"
git commit -m "fix(websocket): handle reconnection on network error"
git commit -m "docs(api): update rate limiting documentation"
git commit -m "test(decomposer): add edge case tests"
git commit -m "refactor(llm): extract provider factory"
```

**Typy:**
- `feat` - nowa funkcjonalność
- `fix` - naprawa błędu
- `docs` - dokumentacja
- `test` - testy
- `refactor` - refaktoryzacja
- `chore` - maintenance

### 4. Pull Request

```bash
# Push brancha
git push -u origin feature/add-langraph-adapter

# Utwórz PR na GitHub
```

**Checklist PR:**
- [ ] Testy przechodzą
- [ ] Linting bez błędów
- [ ] Dokumentacja zaktualizowana
- [ ] PRODUCTION_READINESS.md sprawdzony

---

## Struktura Kodu

### Backend - Dodawanie Endpointu

1. **Schema** (`app/schemas/`)
```python
# app/schemas/new_feature.py
from pydantic import BaseModel

class NewFeatureRequest(BaseModel):
    name: str
    value: int

class NewFeatureResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
```

2. **Route** (`app/api/routes/`)
```python
# app/api/routes/new_feature.py
from fastapi import APIRouter, Depends
from app.schemas.new_feature import NewFeatureRequest, NewFeatureResponse

router = APIRouter(prefix="/new-feature", tags=["new-feature"])

@router.post("/", response_model=NewFeatureResponse)
async def create_feature(request: NewFeatureRequest):
    # implementation
    pass
```

3. **Rejestracja** (`app/api/routes/__init__.py`)
```python
from app.api.routes.new_feature import router as new_feature_router

api_router.include_router(new_feature_router)
```

### Backend - Dodawanie Modelu

1. **Model** (`app/models/`)
```python
# app/models/new_feature.py
from sqlalchemy import Column, String, Integer
from app.models.base import Base

class NewFeature(Base):
    __tablename__ = "new_features"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(Integer, default=0)
```

2. **Migracja**
```bash
cd backend
alembic revision --autogenerate -m "Add new_features table"
alembic upgrade head
```

### Frontend - Dodawanie Komponentu

1. **Types** (`src/types/index.ts`)
```typescript
export interface NewFeature {
  id: string;
  name: string;
  createdAt: string;
}
```

2. **API** (`src/api.ts`)
```typescript
export const createNewFeature = async (data: { name: string; value: number }) => {
  const response = await api.post('/new-feature', data);
  return response.data;
};
```

3. **Component** (`src/components/NewFeature.tsx`)
```typescript
import React from 'react';
import { useMutation } from '@tanstack/react-query';
import { createNewFeature } from '../api';

export const NewFeature: React.FC = () => {
  const mutation = useMutation({
    mutationFn: createNewFeature
  });

  // implementation
};
```

---

## Testowanie

### Uruchamianie Testów

```bash
cd backend

# Wszystkie testy
pytest

# Z verbose output
pytest -v

# Konkretny plik
pytest tests/test_api_tasks.py

# Konkretny test
pytest tests/test_api_tasks.py::test_decompose_task -v

# Z coverage
pytest --cov=app --cov-report=html

# Watch mode (wymaga pytest-watch)
ptw
```

### Pisanie Testów

```python
# tests/test_new_feature.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_new_feature():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/new-feature",
            json={"name": "test", "value": 42},
            headers={"X-API-Key": "test-key"}
        )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test"
```

### Fixtures

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_llm_router():
    router = AsyncMock()
    router.planning_call.return_value = {...}
    return router

@pytest.fixture
async def db_session():
    # Setup test database
    async with get_test_db() as session:
        yield session
```

---

## Debugowanie

### Backend

```python
# Użyj breakpoint()
def some_function():
    breakpoint()  # <- zatrzyma się tutaj
    return result

# Lub logging
import structlog
logger = structlog.get_logger()
logger.info("debug info", variable=value)
```

### VS Code Launch Config

```json
// .vscode/launch.json
{
  "configurations": [
    {
      "name": "Backend",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "cwd": "${workspaceFolder}/agent-orchestrator/backend"
    },
    {
      "name": "Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "cwd": "${workspaceFolder}/agent-orchestrator/backend"
    }
  ]
}
```

---

## Zmienne Środowiskowe

### Backend (.env)

```bash
# === WYMAGANE ===
API_KEY=your-32-character-minimum-api-key
ANTHROPIC_API_KEY=sk-ant-api03-...
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orchestrator
REDIS_URL=redis://localhost:6379

# === OPCJONALNE ===
# CORS - lista dozwolonych origins (JSON array)
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# Budżet dzienny LLM (USD)
DAILY_BUDGET_USD=5.0

# URL do lokalnego LLM (Ollama)
EXECUTION_LLM_URL=http://localhost:11434/v1

# Poziom logowania
LOG_LEVEL=INFO

# Środowisko (development/staging/production)
ENVIRONMENT=development
```

### Frontend

```bash
# .env lub zmienne środowiskowe
VITE_API_URL=http://localhost:8000
```

---

## Docker Development

### Pełne środowisko w Docker

```bash
# Build i start wszystkich usług
docker-compose up --build

# Tylko infrastruktura (DB + Redis)
docker-compose up -d db redis

# Logi
docker-compose logs -f api
docker-compose logs -f frontend

# Shell w kontenerze
docker-compose exec api bash
docker-compose exec db psql -U postgres -d orchestrator
```

### Rebuild po zmianach

```bash
# Rebuild konkretnej usługi
docker-compose up --build api

# Pełny rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

---

## Troubleshooting

### Database Connection Error

```bash
# Sprawdź czy PostgreSQL działa
docker-compose ps db

# Sprawdź logi
docker-compose logs db

# Reset bazy
docker-compose down -v  # UWAGA: usuwa dane!
docker-compose up -d db
```

### Redis Connection Error

```bash
# Sprawdź czy Redis działa
docker-compose ps redis

# Test połączenia
docker-compose exec redis redis-cli ping
```

### Import Errors (Python)

```bash
# Upewnij się, że jesteś w venv
source .venv/bin/activate

# Reinstalacja
pip install -e ".[dev]"
```

### Port Already in Use

```bash
# Znajdź proces
lsof -i :8000
lsof -i :3000

# Zabij proces
kill -9 <PID>
```

### Ollama Not Responding

```bash
# Sprawdź czy Ollama działa
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

---

## Best Practices

### Kod

1. **Typowanie** - używaj type hints wszędzie
2. **Docstrings** - dla publicznych funkcji
3. **Małe funkcje** - jedna odpowiedzialność
4. **Testy** - pisz testy dla nowego kodu
5. **Async** - używaj async/await dla I/O

### Git

1. **Małe commity** - atomowe zmiany
2. **Dobre opisy** - co i dlaczego
3. **Rebase** - przed merge do main
4. **Review** - nie merguj bez review

### Bezpieczeństwo

1. **Nigdy nie commituj sekretów**
2. **Waliduj input użytkownika**
3. **Używaj parametryzowanych queries**
4. **Loguj bez wrażliwych danych**

---

## Powiązane dokumenty

- [Mapa kodu](CODEBASE.md)
- [Dokumentacja API](API.md)
- [Dokumentacja testów](TESTING.md)
- [Wytyczne dla kontrybutorów](../CONTRIBUTING.md)

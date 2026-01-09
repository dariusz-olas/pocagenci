# Dokumentacja Testów - Agent Orchestrator

> **Cel dokumentu:** Strategia testowania, struktura testów, jak pisać i uruchamiać testy.

---

## Przegląd

### Aktualny Stan

| Kategoria | Liczba | Pokrycie | Status |
|-----------|--------|----------|--------|
| Unit testy | 13 | ~30% | 🔴 Niewystarczające |
| Integration testy | 0 | 0% | 🔴 Brak |
| E2E testy | 0 | 0% | 🔴 Brak |

**Cel przed produkcją:** 80% pokrycia kodu

### Narzędzia

| Narzędzie | Cel |
|-----------|-----|
| pytest | Framework testowy |
| pytest-asyncio | Async testy |
| pytest-cov | Coverage |
| httpx | Async HTTP client (testy API) |
| unittest.mock | Mockowanie |

---

## Struktura Testów

```
backend/tests/
├── __init__.py
├── conftest.py              # Globalne fixtures
├── test_api_tasks.py        # Testy API /tasks
├── test_task_decomposer.py  # Unit testy TaskDecomposer
├── test_cost_tracker.py     # Unit testy CostTracker
│
├── unit/                    # (planowane)
│   ├── test_llm_router.py
│   ├── test_execution_engine.py
│   └── test_crewai_adapter.py
│
├── integration/             # (planowane)
│   ├── test_db_operations.py
│   ├── test_redis_cache.py
│   └── test_websocket.py
│
└── e2e/                     # (planowane)
    ├── test_full_flow.py
    └── test_demo_scenarios.py
```

---

## Uruchamianie Testów

### Podstawowe komendy

```bash
cd backend

# Wszystkie testy
pytest

# Z verbose output
pytest -v

# Konkretny plik
pytest tests/test_api_tasks.py

# Konkretny test
pytest tests/test_api_tasks.py::test_decompose_task

# Testy pasujące do wzorca
pytest -k "decompose"
pytest -k "not slow"

# Pokaż print statements
pytest -s

# Zatrzymaj na pierwszym błędzie
pytest -x

# Ostatnie 3 nieudane
pytest --lf
```

### Coverage

```bash
# Raport w terminalu
pytest --cov=app

# Raport HTML
pytest --cov=app --cov-report=html
# Otwórz htmlcov/index.html

# Minimalny próg
pytest --cov=app --cov-fail-under=80
```

### Watch Mode

```bash
# Wymaga pytest-watch
pip install pytest-watch

# Automatyczne uruchamianie po zmianach
ptw

# Z konkretnymi opcjami
ptw -- -v tests/test_api_tasks.py
```

---

## Pisanie Testów

### Struktura Testu

```python
# tests/test_example.py
import pytest
from unittest.mock import AsyncMock, MagicMock

class TestFeatureName:
    """Testy dla konkretnej funkcjonalności."""

    @pytest.fixture
    def setup_data(self):
        """Fixture dla tej klasy testów."""
        return {"key": "value"}

    def test_should_do_something(self, setup_data):
        """Test opisujący oczekiwane zachowanie."""
        # Arrange
        input_data = setup_data

        # Act
        result = function_under_test(input_data)

        # Assert
        assert result == expected_value

    @pytest.mark.asyncio
    async def test_async_operation(self):
        """Test async funkcji."""
        result = await async_function()
        assert result is not None
```

### Nazewnictwo

```python
# Format: test_<co_testujemy>_<scenariusz>_<oczekiwany_wynik>

def test_decompose_task_with_valid_input_returns_subtasks():
    pass

def test_decompose_task_with_empty_description_raises_validation_error():
    pass

def test_cost_tracker_when_budget_exceeded_returns_error():
    pass
```

### Fixtures

```python
# tests/conftest.py - globalne fixtures

import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient
from app.main import app
from app.config import Settings

@pytest.fixture
def settings():
    """Test settings."""
    return Settings(
        api_key="test-api-key-32-characters-long",
        anthropic_api_key="test-anthropic-key",
        database_url="postgresql+asyncpg://test:test@localhost/test",
        redis_url="redis://localhost:6379"
    )

@pytest.fixture
def mock_llm_router():
    """Mock LLM Router dla unit testów."""
    router = AsyncMock()
    router.planning_call.return_value = {
        "subtasks": [
            {"id": "1", "title": "Task 1", "complexity": "simple"}
        ],
        "execution_order": [["1"]],
        "estimated_cost_usd": 0.05
    }
    return router

@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    redis = AsyncMock()
    redis.get.return_value = None
    redis.set.return_value = True
    redis.incrbyfloat.return_value = 1.0
    return redis

@pytest.fixture
async def async_client():
    """Async HTTP client dla testów API."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def auth_headers():
    """Headers z API key."""
    return {"X-API-Key": "test-api-key-32-characters-long"}
```

---

## Kategorie Testów

### Unit Testy

Testują pojedyncze komponenty w izolacji.

```python
# tests/test_task_decomposer.py
import pytest
from unittest.mock import AsyncMock
from app.core.task_decomposer import TaskDecomposer

class TestTaskDecomposer:

    @pytest.fixture
    def decomposer(self, mock_llm_router):
        return TaskDecomposer(llm_router=mock_llm_router)

    @pytest.mark.asyncio
    async def test_decompose_returns_valid_structure(self, decomposer):
        # Arrange
        task_description = "Create a REST API"

        # Act
        result = await decomposer.decompose(task_description)

        # Assert
        assert "subtasks" in result
        assert len(result["subtasks"]) > 0
        assert all("id" in st for st in result["subtasks"])

    @pytest.mark.asyncio
    async def test_decompose_estimates_cost(self, decomposer):
        result = await decomposer.decompose("Simple task")

        assert "estimated_cost_usd" in result
        assert result["estimated_cost_usd"] > 0
```

### Integration Testy

Testują współpracę komponentów.

```python
# tests/integration/test_db_operations.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.models.task import Task
from app.models.base import Base

class TestDatabaseOperations:

    @pytest.fixture
    async def db_session(self):
        """Real database session for integration tests."""
        engine = create_async_engine(
            "postgresql+asyncpg://test:test@localhost/test_db"
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSession(engine) as session:
            yield session

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @pytest.mark.asyncio
    async def test_create_and_retrieve_task(self, db_session):
        # Create
        task = Task(description="Test task")
        db_session.add(task)
        await db_session.commit()

        # Retrieve
        retrieved = await db_session.get(Task, task.id)

        assert retrieved is not None
        assert retrieved.description == "Test task"
```

### API Testy

Testują endpointy HTTP.

```python
# tests/test_api_tasks.py
import pytest
from httpx import AsyncClient

class TestTasksAPI:

    @pytest.mark.asyncio
    async def test_decompose_task_success(self, async_client, auth_headers):
        response = await async_client.post(
            "/api/v1/tasks/decompose",
            json={"description": "Create a user login form"},
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "subtasks" in data
        assert len(data["subtasks"]) > 0

    @pytest.mark.asyncio
    async def test_decompose_task_validation_error(self, async_client, auth_headers):
        # Description too short
        response = await async_client.post(
            "/api/v1/tasks/decompose",
            json={"description": "Hi"},
            headers=auth_headers
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_decompose_task_unauthorized(self, async_client):
        response = await async_client.post(
            "/api/v1/tasks/decompose",
            json={"description": "Create something"}
            # No auth header
        )

        assert response.status_code == 401
```

### WebSocket Testy

```python
# tests/integration/test_websocket.py
import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient
from starlette.websockets import WebSocket

class TestWebSocket:

    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        with TestClient(app) as client:
            with client.websocket_connect("/ws/tasks/test-id") as ws:
                # Connection should be accepted
                data = ws.receive_json()
                assert data["type"] == "connected"

    @pytest.mark.asyncio
    async def test_websocket_receives_progress(self):
        # Trigger task execution and verify WebSocket messages
        pass
```

---

## Mockowanie

### AsyncMock dla async funkcji

```python
from unittest.mock import AsyncMock

mock_service = AsyncMock()
mock_service.method.return_value = {"result": "value"}

# Użycie
result = await mock_service.method()
assert result == {"result": "value"}
```

### Patch dla dependency injection

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_with_patched_dependency():
    mock_router = AsyncMock()
    mock_router.planning_call.return_value = {"subtasks": []}

    with patch("app.dependencies.get_llm_router", return_value=mock_router):
        # Test code using the patched dependency
        pass
```

### MagicMock dla sync obiektów

```python
from unittest.mock import MagicMock

mock_config = MagicMock()
mock_config.api_key = "test-key"
mock_config.daily_budget = 5.0
```

---

## Test Markers

```python
# Definiowanie markerów w pytest.ini lub pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests requiring external services",
    "e2e: marks end-to-end tests",
]
```

```python
# Użycie w testach
@pytest.mark.slow
def test_long_running_operation():
    pass

@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_integration():
    pass

@pytest.mark.e2e
def test_full_user_flow():
    pass
```

```bash
# Uruchamianie z/bez markerów
pytest -m "not slow"           # Pomiń wolne
pytest -m "integration"         # Tylko integracyjne
pytest -m "not integration"     # Bez integracyjnych
```

---

## Testowanie Error Handling

```python
import pytest

class TestErrorHandling:

    @pytest.mark.asyncio
    async def test_raises_validation_error(self, decomposer):
        with pytest.raises(ValueError) as exc_info:
            await decomposer.decompose("")

        assert "description cannot be empty" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_handles_llm_api_error(self, decomposer, mock_llm_router):
        mock_llm_router.planning_call.side_effect = Exception("API Error")

        with pytest.raises(Exception) as exc_info:
            await decomposer.decompose("Valid description")

        assert "API Error" in str(exc_info.value)
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -e ".[dev]"

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379
          API_KEY: test-api-key-32-characters-minimum
          ANTHROPIC_API_KEY: test-key

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Best Practices

### Do's

1. **Izolacja** - każdy test niezależny od innych
2. **Czytelność** - nazwa testu opisuje co testujemy
3. **AAA Pattern** - Arrange, Act, Assert
4. **Małe testy** - jeden test = jedna asercja (gdy możliwe)
5. **Fast** - unit testy < 1s, integration < 10s
6. **Deterministic** - ten sam wynik za każdym razem

### Don'ts

1. **Nie testuj frameworków** - nie testuj FastAPI, SQLAlchemy
2. **Nie testuj bibliotek** - nie testuj Pydantic walidacji
3. **Nie używaj sleep()** - użyj async/await lub mocków
4. **Nie polegaj na kolejności** - testy mogą być równoległe
5. **Nie hardcoduj danych** - używaj fixtures

---

## Planowane Testy

### Priorytet 1 (Przed Demo)

- [ ] `test_execution_engine.py` - testy ExecutionEngine
- [ ] `test_websocket_integration.py` - testy WebSocket
- [ ] `test_background_tasks.py` - testy background execution

### Priorytet 2 (Przed Staging)

- [ ] `test_rate_limiter.py` - testy rate limiting
- [ ] `test_llm_providers.py` - testy providerów LLM
- [ ] `test_crewai_adapter.py` - testy adaptera CrewAI

### Priorytet 3 (Przed Produkcją)

- [ ] `test_e2e_flow.py` - pełny flow użytkownika
- [ ] `test_demo_scenarios.py` - scenariusze z DEMO_SCENARIOS.md
- [ ] `test_error_recovery.py` - odporność na błędy

---

## Powiązane dokumenty

- [Mapa kodu](CODEBASE.md)
- [Wytyczne developmentu](DEVELOPMENT.md)
- [Gotowość produkcyjna](../PRODUCTION_READINESS.md)

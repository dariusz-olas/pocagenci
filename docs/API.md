# Dokumentacja API - Agent Orchestrator

> **Base URL:** `http://localhost:8000/api/v1`
> **Autentykacja:** Header `X-API-Key`
> **Format:** JSON

---

## Autentykacja

Wszystkie endpointy (poza `/health`) wymagają nagłówka `X-API-Key`:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/tasks
```

**Błąd autentykacji:**
```json
{
  "detail": "Invalid API key"
}
```

---

## Endpointy

### Tasks

#### POST /tasks/decompose

Dekompozycja zadania na subtaski przez LLM.

**Request:**
```json
{
  "description": "Create a REST API endpoint for user authentication with JWT tokens"
}
```

**Walidacja:**
- `description`: string, 10-5000 znaków

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Create a REST API endpoint for user authentication with JWT tokens",
  "status": "ready",
  "subtasks": [
    {
      "id": "sub-001",
      "title": "Define User model",
      "description": "Create SQLAlchemy model for User with email and hashed password",
      "complexity": "simple",
      "dependencies": [],
      "acceptance_criteria": [
        "User model has id, email, hashed_password fields",
        "Email is unique"
      ],
      "order_index": 0
    },
    {
      "id": "sub-002",
      "title": "Implement password hashing",
      "description": "Add bcrypt password hashing utility",
      "complexity": "simple",
      "dependencies": ["sub-001"],
      "acceptance_criteria": [
        "Passwords are hashed with bcrypt",
        "Verification function works"
      ],
      "order_index": 1
    }
  ],
  "execution_order": [["sub-001"], ["sub-002", "sub-003"], ["sub-004"]],
  "estimated_cost_usd": 0.042,
  "created_at": "2026-01-09T10:30:00Z"
}
```

**Rate Limit:** 10 requests/minute

---

#### GET /tasks/{task_id}

Pobierz szczegóły zadania.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Create a REST API endpoint...",
  "status": "ready",
  "subtasks": [...],
  "execution_order": [...],
  "estimated_cost_usd": 0.042,
  "created_at": "2026-01-09T10:30:00Z"
}
```

**Response (404):**
```json
{
  "detail": "Task not found"
}
```

---

#### POST /tasks/{task_id}/execute

Uruchom wykonanie zadania przez agenta.

**Response (202):**
```json
{
  "execution_id": "exec-001",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Execution started"
}
```

**Błędy:**
- `400`: Task nie jest w statusie `ready`
- `404`: Task nie istnieje

---

#### GET /tasks

Lista zadań (z paginacją - planowana).

**Query params:**
- `status` (opcjonalny): Filtruj po statusie
- `limit` (opcjonalny): Limit wyników (default: 20)
- `offset` (opcjonalny): Offset (default: 0)

**Response (200):**
```json
{
  "items": [...],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

---

### Executions

#### GET /executions/{execution_id}

Pobierz status wykonania.

**Response (200):**
```json
{
  "id": "exec-001",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "started_at": "2026-01-09T10:35:00Z",
  "completed_at": null,
  "current_subtask": "sub-002",
  "progress_percent": 33,
  "logs": [
    {
      "timestamp": "2026-01-09T10:35:01Z",
      "level": "info",
      "message": "Starting subtask: Define User model"
    },
    {
      "timestamp": "2026-01-09T10:35:30Z",
      "level": "info",
      "message": "Completed subtask: Define User model"
    }
  ],
  "result": null
}
```

**Statusy wykonania:**
- `pending` - Oczekuje na start
- `running` - W trakcie wykonania
- `completed` - Zakończone sukcesem
- `failed` - Zakończone błędem

---

### Costs

#### GET /costs/summary

Podsumowanie kosztów LLM.

**Response (200):**
```json
{
  "today_cloud": 2.34,
  "today_tokens": {
    "input": 125000,
    "output": 45000
  },
  "budget_daily": 5.00,
  "budget_remaining": 2.66,
  "budget_percent_used": 46.8,
  "this_month": {
    "cloud": 45.67,
    "requests": 342
  }
}
```

---

### Health

#### GET /health

Health check (bez autentykacji).

**Response (200):**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "checks": {
    "database": "ok",
    "redis": "ok",
    "llm_planning": "ok",
    "llm_execution": "ok"
  },
  "timestamp": "2026-01-09T10:40:00Z"
}
```

**Response (503):**
```json
{
  "status": "unhealthy",
  "checks": {
    "database": "ok",
    "redis": "error: connection refused",
    "llm_planning": "ok",
    "llm_execution": "ok"
  }
}
```

---

## WebSocket API

### WS /ws/tasks/{task_id}

Real-time updates dla zadania.

**Połączenie:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/tasks/550e8400-e29b-41d4-a716-446655440000');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

**Event types:**

#### status
```json
{
  "type": "status",
  "data": {
    "task_id": "550e8400-...",
    "status": "executing",
    "current_subtask": "sub-002"
  }
}
```

#### log
```json
{
  "type": "log",
  "data": {
    "timestamp": "2026-01-09T10:35:01Z",
    "level": "info",
    "message": "Agent started working on: Define User model"
  }
}
```

#### progress
```json
{
  "type": "progress",
  "data": {
    "task_id": "550e8400-...",
    "completed_subtasks": 2,
    "total_subtasks": 5,
    "percent": 40
  }
}
```

#### complete
```json
{
  "type": "complete",
  "data": {
    "task_id": "550e8400-...",
    "status": "completed",
    "result": {
      "success": true,
      "output": "All subtasks completed successfully"
    }
  }
}
```

#### error
```json
{
  "type": "error",
  "data": {
    "task_id": "550e8400-...",
    "error": "LLM API rate limit exceeded",
    "subtask_id": "sub-003"
  }
}
```

---

## Kody Błędów

### HTTP Status Codes

| Kod | Opis |
|-----|------|
| 200 | OK |
| 201 | Created |
| 202 | Accepted (async operation started) |
| 400 | Bad Request (walidacja) |
| 401 | Unauthorized (brak/zły API key) |
| 404 | Not Found |
| 422 | Unprocessable Entity (Pydantic validation) |
| 429 | Too Many Requests (rate limit) |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### Error Response Format

```json
{
  "error": {
    "code": "BUDGET_EXCEEDED",
    "message": "Daily cloud LLM budget exceeded",
    "details": {
      "current": 5.12,
      "limit": 5.00
    }
  }
}
```

### Error Codes

| Code | Opis |
|------|------|
| `VALIDATION_ERROR` | Błąd walidacji danych wejściowych |
| `TASK_NOT_FOUND` | Zadanie nie istnieje |
| `EXECUTION_NOT_FOUND` | Wykonanie nie istnieje |
| `INVALID_TASK_STATUS` | Nieprawidłowy status zadania dla operacji |
| `BUDGET_EXCEEDED` | Przekroczony dzienny budżet LLM |
| `LLM_API_ERROR` | Błąd API LLM (Claude/Ollama) |
| `RATE_LIMIT_EXCEEDED` | Przekroczony limit requestów |
| `INTERNAL_ERROR` | Wewnętrzny błąd serwera |

---

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| `POST /tasks/decompose` | 10 | 1 minuta |
| Wszystkie inne | 100 | 1 minuta |

**Headers w odpowiedzi:**
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1704795600
```

**Response przy przekroczeniu (429):**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": {
      "retry_after": 45
    }
  }
}
```

---

## Przykłady Użycia

### cURL

```bash
# Dekompozycja zadania
curl -X POST http://localhost:8000/api/v1/tasks/decompose \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"description": "Create a user registration form with email validation"}'

# Pobranie zadania
curl http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-API-Key: your-api-key"

# Uruchomienie wykonania
curl -X POST http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000/execute \
  -H "X-API-Key: your-api-key"

# Sprawdzenie kosztów
curl http://localhost:8000/api/v1/costs/summary \
  -H "X-API-Key: your-api-key"
```

### Python

```python
import httpx

API_URL = "http://localhost:8000/api/v1"
API_KEY = "your-api-key"
headers = {"X-API-Key": API_KEY}

async with httpx.AsyncClient() as client:
    # Dekompozycja
    response = await client.post(
        f"{API_URL}/tasks/decompose",
        json={"description": "Create a REST API for todos"},
        headers=headers
    )
    task = response.json()

    # Wykonanie
    response = await client.post(
        f"{API_URL}/tasks/{task['id']}/execute",
        headers=headers
    )
    execution = response.json()
```

### TypeScript (Frontend)

```typescript
// src/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL + '/api/v1',
  headers: {
    'X-API-Key': import.meta.env.VITE_API_KEY
  }
});

export const decomposeTask = async (description: string) => {
  const response = await api.post('/tasks/decompose', { description });
  return response.data;
};

export const executeTask = async (taskId: string) => {
  const response = await api.post(`/tasks/${taskId}/execute`);
  return response.data;
};

export const getCostSummary = async () => {
  const response = await api.get('/costs/summary');
  return response.data;
};
```

---

## OpenAPI / Swagger

Automatyczna dokumentacja dostępna pod:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## Powiązane dokumenty

- [Architektura systemu](ARCHITECTURE.md)
- [Mapa kodu](CODEBASE.md)
- [Wytyczne developmentu](DEVELOPMENT.md)

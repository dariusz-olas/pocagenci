# Setup Migracji Bazy Danych

## ⚠️ Ważne: DATABASE_URL dla migracji

Gdy uruchamiasz migracje **z hosta** (nie z kontenera Docker), musisz użyć `localhost` zamiast `db` jako hosta.

### Dla aplikacji (w kontenerze Docker):
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/orchestrator
```

### Dla migracji (z hosta):
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orchestrator
```

**Uwaga:** Skrypt `alembic/env.py` automatycznie zamienia `@db:` na `@localhost:` podczas migracji, więc możesz użyć tej samej wartości w `.env`.

---

## 🔧 Instalacja zależności

Migracje wymagają `psycopg2-binary` (synchroniczny sterownik PostgreSQL):

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

To automatycznie zainstaluje `psycopg2-binary`.

---

## ✅ Wykonanie migracji

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```

---

## 🔍 Rozwiązywanie problemów

### Błąd: "No module named 'psycopg2'"
**Rozwiązanie:**
```powershell
pip install psycopg2-binary
```

### Błąd: "could not connect to server"
**Przyczyna:** DATABASE_URL używa `db` zamiast `localhost`
**Rozwiązanie:** Skrypt automatycznie zamienia `@db:` na `@localhost:`, ale możesz też ręcznie zmienić w `.env`

### Błąd: "connection refused"
**Sprawdź:**
1. Czy PostgreSQL działa: `docker-compose ps db`
2. Czy port 5432 nie jest zajęty: `netstat -ano | findstr :5432`
3. Czy DATABASE_URL jest poprawny

---

*Ostatnia aktualizacja: 2026-01-09*


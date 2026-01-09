# Rozwiązywanie Problemów z Docker - Windows ARM64

## ❌ Problem: "unable to get image" / "cannot find the file specified"

### Symptomy:
```
unable to get image 'postgres:16-alpine': error during connect: 
in the default daemon configuration on Windows, the docker client must be run 
with elevated privileges to connect: Get "http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.48/images/postgres:16-alpine/json": 
open //./pipe/docker_engine: The system cannot find the file specified.
```

### Przyczyna:
**Docker Desktop nie jest uruchomiony** lub nie jest poprawnie skonfigurowany.

### Rozwiązanie:

#### Krok 1: Sprawdź czy Docker Desktop jest uruchomiony

```powershell
# Sprawdź status Docker
docker info
```

**Jeśli widzisz błąd:**
- Docker Desktop nie jest uruchomiony

#### Krok 2: Uruchom Docker Desktop

1. **Znajdź Docker Desktop:**
   - Naciśnij `Win + S`
   - Wpisz "Docker Desktop"
   - Kliknij "Docker Desktop"

2. **Poczekaj na pełne uruchomienie:**
   - Ikona Docker Desktop pojawi się w system tray (obok zegara)
   - Ikona powinna być zielona/aktywna
   - Może to zająć 30-60 sekund

3. **Sprawdź status:**
   ```powershell
   docker info
   ```
   **Powinno pokazać:** Informacje o Docker, bez błędów

#### Krok 3: Sprawdź czy Docker Desktop działa

```powershell
# Test podstawowy
docker run hello-world
```

**Oczekiwany wynik:** Kontener się uruchomi i pokaże wiadomość "Hello from Docker!"

#### Krok 4: Spróbuj ponownie

```powershell
.\setup-windows.ps1 docker-up
```

---

## ⚠️ Problem: Ostrzeżenie o `version` w docker-compose.yml

### Symptomy:
```
level=warning msg="the attribute `version` is obsolete, it will be ignored"
```

### Rozwiązanie:
To tylko ostrzeżenie, nie błąd. Możesz zignorować lub usunąć linię `version: '3.8'` z `docker-compose.yml` (już naprawione w najnowszej wersji).

---

## 🔧 Problem: Docker Desktop nie uruchamia się

### Sprawdź:

1. **Czy masz Docker Desktop dla ARM64?**
   - Docker Desktop powinien być zainstalowany dla Windows ARM64
   - Sprawdź w ustawieniach Docker Desktop → About

2. **Czy WSL2 jest włączony?**
   ```powershell
   wsl --status
   ```
   - Jeśli nie jest zainstalowany, Docker Desktop go zainstaluje automatycznie

3. **Czy masz wystarczająco zasobów?**
   - Docker Desktop wymaga minimum 4GB RAM
   - Sprawdź w Docker Desktop → Settings → Resources

4. **Restart Docker Desktop:**
   - Kliknij prawym na ikonę Docker Desktop w system tray
   - Wybierz "Restart Docker Desktop"

---

## 🚀 Alternatywa: Użyj opcji hybrydowej

Jeśli Docker Desktop sprawia problemy, możesz użyć infrastruktury w Docker, a aplikacje uruchomić natywnie:

### Opcja 1: Tylko infrastruktura w Docker

```powershell
# Uruchom tylko PostgreSQL i Redis
docker-compose up -d db redis

# Sprawdź czy działają
docker-compose ps

# Uruchom backend natywnie
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000

# W innym terminalu - frontend natywnie
cd frontend
npm run dev
```

### Opcja 2: Wszystko natywnie (wymaga lokalnej instalacji)

Jeśli masz PostgreSQL i Redis zainstalowane lokalnie:

1. **PostgreSQL:**
   - Pobierz dla Windows ARM64: https://www.postgresql.org/download/windows/
   - Utwórz bazę `orchestrator`
   - Zaktualizuj `DATABASE_URL` w `backend\.env`

2. **Redis:**
   - Użyj Docker tylko dla Redis: `docker run -d -p 6379:6379 redis:7-alpine`
   - LUB zainstaluj Redis dla Windows (jeśli dostępny)

---

## 🔍 Diagnostyka

### Sprawdź status Docker

```powershell
# Podstawowe informacje
docker info

# Lista kontenerów
docker ps -a

# Lista obrazów
docker images

# Logi Docker Desktop
# Otwórz Docker Desktop → Settings → Troubleshoot → View logs
```

### Sprawdź porty

```powershell
# Sprawdź czy porty są zajęte
netstat -ano | findstr :5432  # PostgreSQL
netstat -ano | findstr :6379  # Redis
```

### Sprawdź logi kontenerów

```powershell
# Logi PostgreSQL
docker-compose logs db

# Logi Redis
docker-compose logs redis

# Wszystkie logi
docker-compose logs
```

---

## ✅ Checklist: Czy Docker działa?

- [ ] Docker Desktop jest uruchomiony (ikona w system tray)
- [ ] `docker info` działa bez błędów
- [ ] `docker run hello-world` działa
- [ ] `docker-compose --version` pokazuje wersję
- [ ] Porty 5432 i 6379 nie są zajęte przez inne procesy

---

## 📞 Jeśli nadal nie działa

1. **Sprawdź dokumentację Docker Desktop:**
   - https://docs.docker.com/desktop/install/windows-install/

2. **Sprawdź wymagania systemowe:**
   - Windows 10/11 ARM64
   - WSL2 enabled
   - Minimum 4GB RAM

3. **Użyj opcji hybrydowej:**
   - Infrastruktura w Docker (jeśli działa)
   - Aplikacje natywnie (zawsze działa)

---

*Ostatnia aktualizacja: 2026-01-09*


# Wytyczne dla Kontrybutorów

> Dziękujemy za zainteresowanie rozwojem Agent Orchestrator!

---

## Szybki Start

1. **Fork repozytorium** na GitHub
2. **Sklonuj fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pocagenci.git
   cd pocagenci
   ```
3. **Utwórz branch:**
   ```bash
   git checkout -b feature/twoja-funkcjonalnosc
   ```
4. **Setup środowiska:** Zobacz [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
5. **Wprowadź zmiany i przetestuj**
6. **Utwórz Pull Request**

---

## Przed Rozpoczęciem Pracy

### Sprawdź istniejące zasoby

1. **[PRODUCTION_READINESS.md](PRODUCTION_READINESS.md)** - może problem jest już zidentyfikowany
2. **[TASKS.md](TASKS.md)** - może task jest już zaplanowany
3. **GitHub Issues** - może ktoś już nad tym pracuje

### Dla Asystentów AI

Przeczytaj najpierw **[AI.md](AI.md)** - zawiera specyficzne wytyczne dla Claude, Cursor, Copilot.

---

## Typy Kontrybucji

### Bug Fix

1. Utwórz issue z opisem buga
2. Branch: `fix/krotki-opis`
3. Napisz test reprodukujący bug
4. Napraw bug
5. Upewnij się, że wszystkie testy przechodzą

### Nowa Funkcjonalność

1. Otwórz dyskusję w Issues
2. Poczekaj na akceptację pomysłu
3. Branch: `feature/nazwa-funkcjonalnosci`
4. Implementuj z testami
5. Zaktualizuj dokumentację

### Dokumentacja

1. Branch: `docs/co-dokumentujesz`
2. Zmiany w odpowiednich plikach `.md`
3. Nie zmieniaj struktury bez dyskusji

### Refaktoryzacja

1. Otwórz issue z uzasadnieniem
2. Branch: `refactor/co-refaktoryzujesz`
3. Nie zmieniaj zachowania (testy muszą przechodzić)
4. Małe, atomowe commity

---

## Standardy Kodu

### Python (Backend)

```python
# Formatowanie: Black + isort
# Linting: ruff
# Type checking: mypy

# Typowanie
def calculate_cost(tokens: int, price_per_million: float) -> float:
    """
    Kalkuluje koszt na podstawie liczby tokenów.

    Args:
        tokens: Liczba tokenów
        price_per_million: Cena za milion tokenów

    Returns:
        Koszt w USD
    """
    return (tokens / 1_000_000) * price_per_million

# Async/await dla I/O
async def fetch_data() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### TypeScript (Frontend)

```typescript
// Formatowanie: Prettier
// Linting: ESLint

// Typowanie
interface Task {
  id: string;
  description: string;
  status: TaskStatus;
}

// Funkcyjne komponenty
const TaskCard: React.FC<{ task: Task }> = ({ task }) => {
  return <div>{task.description}</div>;
};
```

### Uruchom przed commitem

```bash
# Backend
cd backend
ruff check .
ruff format .
mypy app/

# Frontend
cd frontend
npm run lint
npm run format
```

---

## Commit Messages

### Format

```
type(scope): krótki opis

Dłuższy opis jeśli potrzebny.

Closes #123
```

### Typy

| Typ | Opis |
|-----|------|
| `feat` | Nowa funkcjonalność |
| `fix` | Naprawa błędu |
| `docs` | Dokumentacja |
| `test` | Testy |
| `refactor` | Refaktoryzacja (bez zmiany zachowania) |
| `style` | Formatowanie (bez zmiany logiki) |
| `chore` | Maintenance, dependencies |
| `perf` | Optymalizacja wydajności |

### Scope

| Scope | Opis |
|-------|------|
| `api` | Endpointy REST |
| `ws` | WebSocket |
| `llm` | Integracja LLM |
| `db` | Baza danych |
| `ui` | Frontend |
| `docker` | Konteneryzacja |
| `ci` | CI/CD |

### Przykłady

```bash
git commit -m "feat(api): add pagination to tasks endpoint"
git commit -m "fix(ws): handle reconnection on network error"
git commit -m "docs(api): update rate limiting documentation"
git commit -m "test(decomposer): add edge case tests"
git commit -m "refactor(llm): extract provider factory"
```

---

## Pull Request

### Checklist

- [ ] Branch jest aktualny z `main`
- [ ] Wszystkie testy przechodzą (`make test`)
- [ ] Linting bez błędów (`make lint`)
- [ ] Nowy kod ma testy
- [ ] Dokumentacja zaktualizowana
- [ ] Commit messages zgodne z konwencją

### Tytuł PR

```
type(scope): Krótki opis zmian

Przykłady:
feat(api): Add user authentication endpoint
fix(ws): Resolve memory leak in connection manager
docs(setup): Update Docker installation guide
```

### Opis PR

```markdown
## Opis
Krótki opis co zostało zmienione i dlaczego.

## Typ zmiany
- [ ] Bug fix
- [ ] Nowa funkcjonalność
- [ ] Dokumentacja
- [ ] Refaktoryzacja

## Jak testować
1. Krok 1
2. Krok 2
3. Oczekiwany wynik

## Powiązane Issues
Closes #123
Related to #456

## Screenshots (jeśli UI)
...
```

---

## Code Review

### Dla Autorów

1. **Odpowiadaj na komentarze** - nawet jeśli to tylko "Done" lub "Fixed"
2. **Nie bierz do siebie** - review dotyczy kodu, nie Ciebie
3. **Małe PR-y** - łatwiejsze do review

### Dla Reviewerów

1. **Bądź konstruktywny** - zaproponuj rozwiązanie
2. **Doceniaj** - wskaż co jest dobre
3. **Pytaj** - jeśli nie rozumiesz, zapytaj
4. **Nie blokuj** - drobne nits nie powinny blokować merge

### Etykiety Review

- `MUST`: Musi być naprawione przed merge
- `SHOULD`: Powinno być naprawione, ale nie blokuje
- `NIT`: Drobnostka, nice-to-have
- `QUESTION`: Pytanie, nie wymaga zmiany

---

## Bezpieczeństwo

### NIE commituj

- Kluczy API (`.env`, credentials)
- Haseł
- Tokenów
- Prywatnych kluczy

### Zawsze

- Używaj parametryzowanych queries
- Waliduj input użytkownika
- Sprawdzaj uprawnienia
- Loguj bez wrażliwych danych

### Znalazłeś lukę?

Nie twórz publicznego issue. Skontaktuj się bezpośrednio z maintainerami.

---

## Struktura Projektu

```
pocagenci/
├── AI.md                     # Wytyczne dla AI asystentów
├── CONTRIBUTING.md           # TEN PLIK
├── docs/                     # Dokumentacja
│   ├── ARCHITECTURE.md       # Architektura
│   ├── API.md               # Dokumentacja API
│   ├── CODEBASE.md          # Mapa kodu
│   ├── DEVELOPMENT.md       # Setup developmentu
│   └── TESTING.md           # Dokumentacja testów
│
├── PLAN_DEVELOPMENT.md       # Plan architekturalny
├── PRODUCTION_READINESS.md   # Ocena gotowości
├── TASKS.md                  # Lista zadań
│
└── agent-orchestrator/       # Kod aplikacji
    ├── backend/             # Python FastAPI
    └── frontend/            # React TypeScript
```

---

## Potrzebujesz Pomocy?

1. **Dokumentacja:** Przeczytaj [docs/](docs/)
2. **Issues:** Sprawdź istniejące lub utwórz nowe
3. **Dyskusje:** Otwórz dyskusję na GitHub

---

## Licencja

Wnosząc kod do tego projektu, zgadzasz się, że Twoje kontrybucje będą licencjonowane na tej samej licencji co projekt (MIT).

---

*Dziękujemy za Twoją kontrybucję!*

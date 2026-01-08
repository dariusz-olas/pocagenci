# Agent Orchestrator - Scenariusze Demo

## Przygotowanie

1. Uruchom infrastrukturę:
   ```bash
   make docker-up
   ```

2. Uruchom migracje:
   ```bash
   make migrate
   ```

3. Uruchom backend:
   ```bash
   make dev-backend
   ```

4. Uruchom frontend:
   ```bash
   make dev-frontend
   ```

5. (Opcjonalnie) Uruchom Ollama z modelem:
   ```bash
   ollama run qwen2.5-coder:32b
   ```

---

## Scenariusz 1: Prosty REST API

**Zadanie:** "Create a FastAPI endpoint that returns a list of users from a PostgreSQL database"

**Oczekiwany wynik:**
- 4-6 subtasków
- Complexity: 2 simple, 2-3 medium, 0-1 complex
- Koszt decompose: < $0.05

**Kroki:**
1. Otwórz http://localhost:3000
2. Wpisz zadanie w polu tekstowym
3. Kliknij "Decompose Task"
4. Sprawdź czy subtaski pojawiły się na TaskBoard

---

## Scenariusz 2: Refactoring kodu

**Zadanie:** "Refactor the authentication module to use JWT tokens instead of session cookies, maintaining backward compatibility"

**Oczekiwany wynik:**
- 5-8 subtasków
- Zawiera subtask "complex" dla architektury
- Execution order z zależnościami

---

## Scenariusz 3: Bug fix

**Zadanie:** "Fix the race condition in the order processing service that causes duplicate orders when users double-click the submit button"

**Oczekiwany wynik:**
- 3-5 subtasków
- Zawiera: analiza, implementacja, testy

---

## Scenariusz 4: Nowa funkcjonalność

**Zadanie:** "Add a dark mode toggle to the React application with system preference detection and local storage persistence"

**Oczekiwany wynik:**
- 4-6 subtasków
- Równoległe subtaski dla CSS i logiki

---

## Scenariusz 5: Test budżetu

**Zadanie:** Wykonaj 50+ dekompozycji aby sprawdzić czy budżet się wyczerpie.

**Oczekiwany wynik:**
- CostDashboard pokazuje rosnące koszty
- Po przekroczeniu $5: błąd 402 Payment Required

---

## Weryfikacja sukcesu POC

- [ ] `/tasks/decompose` zwraca JSON w <10s
- [ ] WebSocket pokazuje "connected"
- [ ] CostDashboard aktualizuje się co 30s
- [ ] Wszystkie 5 scenariuszy działa
- [ ] Koszt pojedynczej dekompozycji < $0.10

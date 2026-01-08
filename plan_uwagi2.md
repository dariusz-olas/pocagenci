# Analiza Planu i Rekomendacje dla POC Agent Orchestrator

Poniżej znajdują się kluczowe spostrzeżenia i uwagi techniczne po analizie `plan.md`. Celem jest optymalizacja procesu tworzenia POC (Proof of Concept), aby dostarczyć działający prototyp jak najszybciej, minimalizując ryzyko "utknięcia" w konfiguracji infrastruktury.

## 1. Strategia "MVP First" - Redukcja Zakresu
Plan jest bardzo ambitny i zakłada stworzenie "meta-frameworka" integrującego 4 różne biblioteki agentowe. Dla POC jest to ryzykowne.

**Rekomendacja:**
*   **Wybór jednego adaptera wiodącego:** Na start zaimplementujmy **tylko CrewAI** (lub LangGraph). Pozostałe adaptery (`autogen`, `agency_swarm`) powinny być zdefiniowane tylko jako interfejsy (stubs/mocks), aby udowodnić architekturę pluginową, ale bez pełnej implementacji.
*   **Uzasadnienie:** Każdy framework ma inną logikę zarządzania stanem i pętlą zdarzeń. Próba zgrania czterech naraz na etapie POC może sparaliżować development.

## 2. Infrastruktura LLM (Execution Tier)
Plan zakłada skomplikowaną orkiestrację GPU na RunPod/Vast.ai (scale-to-zero, pre-warming).

**Rekomendacja:**
*   **Abstrakcja zamiast DevOps:** Zamiast pisać kod do zarządzania infrastrukturą RunPod (`gpu_manager.py`) w pierwszej fazie, użyjmy po prostu **OpenRouter** lub innego taniego providera API, który udostępnia modele open-source (Qwen/DeepSeek) w formacie kompatybilnym z OpenAI.
*   **Dlaczego:** Pozwoli to skupić się na logice aplikacji (Orkiestratorze), a nie na debugowaniu API RunPoda i czasu wstawania kontenerów. Kod do zarządzania infrastrukturą można dodać w Fazie 2.
*   **Dev Environment:** Zalecam wsparcie dla lokalnego **Ollama** lub **LM Studio** jako domyślnego "Execution Tier" dla developera.

## 3. Zarządzanie Stanem i Baza Danych
Użycie PostgreSQL + SQLAlchemy + Alembic jest solidne, ale dla szybkiego POC może być overkill.

**Rekomendacja:**
*   **Start z SQLite:** Użyjmy SQLite w trybie asynchronicznym (aiosqlite). SQLAlchemy pozwala na łatwą migrację na Postgres później. To drastycznie uprości setup (brak konieczności stawiania kontenera DB do każdego uruchomienia testów).
*   **Redis:** Jest niezbędny do kolejkowania zadań (Celery/ARQ), więc musi zostać, ale warto rozważyć użycie prostej kolejki w pamięci (in-memory) dla trybu "dev", jeśli nie chcemy polegać na Dockerze przy każdym uruchomieniu.

## 4. Frontend i Komunikacja
Stack (Vite, React, Tailwind) jest poprawny.

**Spostrzeżenia:**
*   **WebSockets:** Plan zakłada real-time updates (`progress.py`). To kluczowe dla UX przy długo działających agentach. Należy upewnić się, że `TaskExecutor` poprawnie emituje zdarzenia do warstwy WebSocket.
*   **Logs Streaming:** Agenci generują dużo logów. Warto od razu przemyśleć mechanizm strumieniowania ich do UI, zamiast trzymać w bazie i odpytywać (polling).

## 5. Konkretne uwagi do kodu (z planu)

### `LLMRouter`
*   Kod w planie używa `httpx` bezpośrednio. Sugeruję użycie biblioteki `litellm` lub `langchain`, które standaryzują obsługę błędów i różnice w API między providerami (Anthropic vs OpenAI vs Azure vs vLLM). Ręczna obsługa `httpx` dla każdego providera to proszenie się o kłopoty przy zmianach API.

### `TaskDecomposer`
*   Prompt jest kluczowy. Należy zadbać o to, by output był *zawsze* poprawnym JSONem. Warto użyć bibliotek typu `instructor` lub `pydantic` features w LangChain do wymuszania schematu (Structured Output), zamiast polegać tylko na prompcie.

## 6. Plan Działania (Revised)

1.  **Setup Projektu:** FastAPI + SQLite + Podstawowa struktura katalogów.
2.  **Core Logic:** Implementacja `TaskDecomposer` (z użyciem mocka lub API OpenAI zamiast Claude na start).
3.  **Adapter CrewAI:** Implementacja jednego działającego adaptera.
4.  **API & WebSocket:** Wystawienie endpointów dla UI.
5.  **Frontend:** Prosty dashboard do zlecania zadań i podglądu logów.
6.  **Refactor & Infra:** Dopiero wtedy dodanie obsługi RunPod i innych adapterów.

---
**Podsumowanie:** Budujmy system modułowy, ale zacznijmy od jednej, działającej ścieżki (tzw. Steel Thread): User Request -> Decomposer -> CrewAI Agent -> Wynik.


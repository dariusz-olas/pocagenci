## Cel tego pliku

Ten dokument zbiera **uwagi do `plan.md`**: niejasności, ryzyka, sprzeczności i decyzje, które trzeba doprecyzować **zanim** zaczniesz kodować POC. Traktuj to jako checklistę “co może pójść źle / co trzeba ustalić”, żeby POC wyszedł szybko i stabilnie.

---

## Najważniejsza obserwacja (meta)

- **`plan.md` to bardziej “kompletny prompt / blueprint” niż plan POC**: zawiera docelową architekturę (API + worker + frontend + infra + 4 frameworki) oraz przykładowe fragmenty kodu, ale brakuje definicji “co dokładnie ma działać w POC” i jakie są kryteria sukcesu.
- **Skala**: w jednej iteracji chcesz złożyć FastAPI + task mgmt + websockets + DB + redis + worker + routing LLM + kosztomierz + integracje z 4 frameworkami + infra (RunPod/Terraform/Hetzner) + frontend. To jest za szerokie jak na POC, jeśli ma powstać szybko i bez długiego długu technicznego.

Rekomendacja: przed kodowaniem POC ustal **MVP POC** (patrz sekcja “Proponowany zakres POC”).

---

## Proponowany zakres POC (żeby dowieźć wartość szybko)

### Minimum, które realnie “udowadnia” koncepcję

- **1 ścieżka end-to-end**:
  - `POST /tasks/decompose` → dostajesz `TaskDecomposition` (JSON) z listą subtasków i zależnościami
  - `POST /tasks/{id}/execute` → odpala wykonanie (nawet jeśli “execution” jest na początku mockowane)
  - **progress** (SSE albo WebSocket) → frontend widzi status/logi
- **2 tryby LLM**:
  - **planning**: 1 provider (na start: OpenAI *albo* Anthropic), tylko do decomposera
  - **execution**: 1 provider (na start: lokalny OpenAI-compatible endpoint *albo* zwykły mock), do “wykonania” subtasków
- **0–1 framework agentowy** na start:
  - Zacznij od **jednego** adaptera (np. CrewAI *albo* LangGraph). Reszta jako “placeholdery”/interfejsy.

### Co odłożyć poza POC (albo zrobić jako “stuby”)

- Terraform/Hetzner/Vast.ai/Kubernetes/monitoring pełne → **po POC**
- Pełne “cost optimization” z daily budget + GPU manager → w POC tylko **metryki** i proste progi
- 4 adaptery naraz → **nie**, bo integracje i kompatybilność wersji zabiją tempo

---

## Kryteria sukcesu POC (do doprecyzowania)

Bez tego łatwo “utknąć w architekturze”.

- **Co jest “done”?**
  - Czy wystarczy decomposer + proste wykonanie, czy musi generować pliki/kod w repo?
- **Jak mierzymy sukces?**
  - np. czas od wpisania zadania do powstania subtasków < X sekund
  - koszt decomposera < $Y / zadanie
  - execution: % poprawnych wyników na 3–5 scenariuszach demo
- **Jaki poziom trwałości danych?**
  - Czy POC wymaga Postgresa i migracji, czy wystarczy SQLite/in-memory?

---

## Kluczowe niejasności / decyzje do podjęcia (przed kodem)

### Warstwa “Task Management”

- **Model danych tasków**:
  - Brakuje jednoznacznych pól: statusy, retry, owner, timestamps, error, idempotency key.
- **Zależności i harmonogram**:
  - `execution_order: List[List[str]]` sugeruje batch’e równoległe, ale nie ma definicji “kiedy task uznajemy za gotowy” ani jak obsługujemy partial failure.
- **Idempotencja**:
  - Czy `POST /tasks/decompose` dla identycznego inputu ma tworzyć nowy task czy zwracać istniejący?

### Queue/Worker

- Plan miesza pojęcia: `Celery/ARQ worker` + w docker-compose jest `arq ...`.
  - **Decyzja**: ARQ czy Celery? ARQ (async + Redis) jest spójniejsze z FastAPI async i prostsze na POC.
- **Retry/backoff/dead-letter**:
  - Brak zasad retry (ile, kiedy, dla jakich błędów).

### Real-time updates

- Jest wzmianka o websocketach (`backend/app/api/websockets/progress.py`), ale brak:
  - kontraktu eventów (typy eventów, payload, kolejność)
  - mapowania eventów do tasków/execów (channel per task? per user? global?)
  - auth do socketów (w POC może być “bez auth”, ale warto to jawnie zaznaczyć).

---

## Uwagi do pokazanych fragmentów kodu (ryzyka implementacyjne)

### Async vs sync (największe ryzyko)

- W przykładzie `CrewAIAdapter._create_llm_wrapper` jest `asyncio.run(...)` w metodzie `_call`.
  - To **pęknie** w środowisku, gdzie już działa event loop (FastAPI/uvicorn) albo doprowadzi do blokad.
  - POC powinien konsekwentnie rozdzielić:
    - sync API frameworków (CrewAI) → uruchamiane w `anyio.to_thread.run_sync(...)` / threadpool
    - async I/O (HTTP do LLM) → normalnie `await`.
- `Crew.kickoff()` jest sync — jeśli uruchomisz go w endpointcie async bez threadpoola, zablokujesz serwer.

### Niespójności w endpointach/portach (łatwe do przeoczenia)

- W `LLMRouter` przykład mówi o `VLLMClient(config.vllm_endpoint)  # localhost:8000`, ale w `docker-compose.yml` jest `VLLM_ENDPOINT=http://host.docker.internal:8080`.
  - **Decyzja**: jeden port/URL i jedna nazwa zmiennej (`VLLM_ENDPOINT`), inaczej POC zacznie się od “dlaczego nie działa?”.
- Frontend w compose ma `ports: "3000:3000"`, ale Vite domyślnie startuje na `5173` (chyba że jawnie skonfigurujesz).
  - Jeśli POC ma działać “od strzała”, doprecyzuj port i komendę uruchomieniową obrazu frontu.

### “Planning tier <5% wywołań”

- To jest cel produktowy, ale w POC trzeba doprecyzować:
  - co liczymy jako “wywołanie”
  - czy decomposer zawsze używa planning, czy tylko czasem
  - jak fallbackujemy, gdy brak klucza API / limit / błąd.

### “Execution tier koszt = 0”

- W kodzie `execution_call` koszt ustawiony na 0.0, ale:
  - RunPod/Vast.ai to realny koszt (czas GPU, cold start, ewentualnie request-based).
  - Nawet jeśli nie rozliczasz per-token, **POC powinien logować “koszt infrastruktury”** osobno (czas, godziny).

### Token estimation

- `self._estimate_tokens(prompt)` jest w przykładzie, ale brak implementacji.
  - Na POC: albo proste przybliżenie (len/4), albo realny tokenizer (zależnie od providerów).
  - Ważne: różne modele mają różne tokenizery — to zawsze będzie przybliżenie.

### RunPod API / endpoints

- W przykładzie jest `GET .../health` i `POST .../scale` dla endpointu serverless.
  - To zależy od faktycznego API RunPod; w POC trzeba to zweryfikować i mieć “feature flag” na integrację.
- `stop: ["```\n\n", "</code>"]` jest arbitralne — może ucinać odpowiedzi. Na POC lepiej nie robić agresywnych stopów, tylko walidować output.

### Nazwy modeli / “Claude Opus 4.5”

- W planie pada `Claude Opus 4.5 / GPT-4 / DeepSeek-V3` — to brzmi jak skrót myślowy, ale w implementacji musisz mieć:
  - **konkretne** nazwy modeli dostępne u providera (i ich limity)
  - mapowanie “tier → provider → model”
  - jasne fallbacki, gdy model niedostępny.

---

## Spójność technologiczna / wersje bibliotek (do ustalenia)

Plan zakłada:

- **Python 3.11+**
- **Pydantic v2**
- **FastAPI async**

Potencjalne tarcia:

- **LangChain / CrewAI**: część ekosystemu długo była “przywiązana” do Pydantic v1 lub miała okresy przejściowe.
  - W POC: pinuj wersje zależności i testuj minimalny flow.
- **LangGraph/AutoGen/Agency Swarm**: integracje mają różne style (sync/async, własne modele danych).
  - W POC: adaptery jako cienkie “anti-corruption layer”, bez prób ujednolicenia wszystkiego naraz.

---

## API kontrakty (brakuje w `plan.md`)

Żeby frontend mógł powstać bez zgadywania, potrzebujesz specyfikacji:

- **Endpointy** (przykładowe):
  - `POST /tasks/decompose` (input: opis; output: decomposition + id)
  - `POST /tasks/{id}/execute` (start; output: execution id)
  - `GET /tasks/{id}` / `GET /executions/{id}`
  - `GET /costs/summary`
- **Schematy błędów**:
  - spójny format (np. `code`, `message`, `details`), mapowanie wyjątków z providerów.
- **Autoryzacja**:
  - w POC można “no-auth”, ale wpisz to jawnie i zabezpiecz chociaż klucze API po stronie serwera (nigdy w froncie).

---

## Bezpieczeństwo / compliance (minimum na POC)

- **Sekrety**: klucze API tylko po stronie backendu; `.env` lokalnie, w prod secrets manager/ENV.
- **Logowanie promptów**:
  - Ustal czy logujesz pełne prompty i odpowiedzi. Domyślnie: **nie loguj pełnej treści** lub loguj z maskowaniem, bo mogą zawierać dane wrażliwe.
- **SSRF / egress**:
  - Jeśli dopuszczasz narzędzia “web” lub “git”, ogranicz domeny/hosty.

---

## Observability (żeby debugowanie nie bolało)

Minimalny zestaw na POC:

- **Correlation IDs**: `task_id`, `execution_id`, `subtask_id` w każdym logu.
- **Event log**: progres w postaci zdarzeń (append-only) zamiast “nadpisywania statusu”.
- **Metryki**:
  - latency per endpoint
  - latency per provider
  - liczniki błędów per provider
  - koszt cloud (tokens) + koszt GPU (czas).

---

## Architektura danych / storage (POC-friendly)

- Plan sugeruje Postgres + Alembic + SQLAlchemy, ale POC może zacząć od:
  - SQLite + migracje minimalne (albo nawet in-memory) — jeśli priorytetem jest szybkość
  - Postgres od razu — jeśli priorytetem jest “jak w produkcji”.
- **Decyzja**: czy historia wykonań ma być trwała? (to wpływa na UI: ExecutionLog, TaskBoard).

---

## UI (frontend) — co jest niedopowiedziane

- W przykładach komponentów są wywołania `api.post('/tasks/decompose', ...)` i `api.get('/costs/summary')`, ale:
  - brak definicji `api` (axios? fetch wrapper?)
  - brak kontraktów odpowiedzi
  - brak UX dla błędów (limit budżetu, brak endpointu execution, cold start).

Rekomendacja POC: najpierw ustalić **contract-first** (schematy Pydantic → OpenAPI), a dopiero potem UI.

---

## Deployment/infra — uwagi praktyczne

- `docker-compose.yml` zakłada `host.docker.internal` dla `VLLM_ENDPOINT`.
  - Na Windows to zwykle działa, ale w zależności od środowiska może wymagać dopięcia sieci. Dla POC warto mieć możliwość ustawienia endpointu jako zwykły URL bez “magii”.
- Plan zawiera Terraform i zasoby Hetzner/RunPod, ale na POC:
  - najpierw zrób “local happy path” z mockami providerów
  - dopiero potem włączaj prawdziwe integracje (feature flag).

---

## Rekomendowane “feature flags” (żeby nie utknąć)

- `ENABLE_REAL_LLM_PLANNING` (mock decomposera vs real)
- `ENABLE_EXECUTION_PROVIDER_RUNPOD`
- `ENABLE_WEBSOCKETS` (fallback do SSE/pollingu)
- `ENABLE_DB_PERSISTENCE` (in-memory vs Postgres)

---

## Szybka checklista przed startem kodowania

- [ ] Zdefiniowane **MVP POC** + 3–5 scenariuszy demo
- [ ] Ustalony **jeden** planning provider i **jeden** execution provider (lub mock)
- [ ] Wybrany queue system (ARQ vs Celery) + zasady retry
- [ ] Spisane kontrakty API (endpointy + schematy + błędy)
- [ ] Ustalony model statusów task/execution/subtask
- [ ] Rozstrzygnięte: WebSocket vs SSE (i format eventów)
- [ ] Pin wersji zależności (Pydantic v2 + kompatybilność frameworków)
- [ ] Polityka logów: co logujemy (i co maskujemy)



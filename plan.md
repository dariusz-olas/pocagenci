# 🚀 AGENT ORCHESTRATOR - Kompletny Prompt dla Claude Code

## Kontekst projektu

Budujesz **AgentOrchestrator** - meta-framework który łączy najlepsze funkcje z LangGraph, CrewAI, AutoGen i Agency Swarm, z hybrydową architekturą LLM (płatny cloud do planowania + self-hosted do wykonania) i systemem task management.

---

## 🎯 GŁÓWNE WYMAGANIA

### 1. Architektura hybrydowa LLM

```
PLANNING TIER (Cloud API - płatny, używany oszczędnie)
├── Claude Opus 4.5 / GPT-4 / DeepSeek-V3 API
├── Zastosowanie: rozbijanie tasków, architektura, code review, decyzje routingu
└── Cel: <5% wszystkich wywołań LLM

EXECUTION TIER (Self-hosted - darmowy, główny workhorse)
├── Qwen2.5-Coder-32B lub DeepSeek-Coder-V2
├── Hosting: RunPod / Vast.ai (on-demand) lub lokalny GPU
└── Zastosowanie: implementacja, testy, refactoring, boilerplate
```

### 2. Integracja frameworków agentowych

```
AgentOrchestrator (Twój kod)
├── LangGraph Adapter  → grafy stanów, checkpointing, human-in-the-loop
├── CrewAI Adapter     → role-based agents, hierarchiczna delegacja
├── AutoGen Adapter    → konwersacyjna współpraca, group chat
└── Agency Swarm Adapter → lekkie narzędzia, custom tools
```

### 3. Task Management System

```
User Input → Task Parser → Decomposer → Dependency Resolver → Agent Assigner → Executor → Progress Tracker
```

---

## 📁 STRUKTURA PROJEKTU

```
agent-orchestrator/
├── docker-compose.yml              # Lokalne środowisko dev
├── docker-compose.prod.yml         # Produkcja
├── Dockerfile.api                  # Backend API
├── Dockerfile.worker               # Worker do task execution
├── Makefile                        # Komendy dev/deploy
│
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf                 # Główna konfiguracja
│   │   ├── runpod.tf               # RunPod GPU instances
│   │   ├── vastai.tf               # Vast.ai alternatywa
│   │   ├── hetzner.tf              # Tani VPS dla API/DB
│   │   └── variables.tf
│   ├── kubernetes/
│   │   ├── api-deployment.yaml
│   │   ├── worker-deployment.yaml
│   │   ├── redis-statefulset.yaml
│   │   └── ingress.yaml
│   └── scripts/
│       ├── setup-runpod.sh         # Provisioning GPU
│       ├── deploy-model.sh         # Deploy Qwen/DeepSeek
│       └── health-check.sh
│
├── backend/
│   ├── pyproject.toml
│   ├── alembic/                    # DB migrations
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Pydantic settings
│   │   ├── dependencies.py
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── tasks.py        # CRUD tasks
│   │   │   │   ├── agents.py       # Agent management
│   │   │   │   ├── executions.py   # Execution history
│   │   │   │   └── webhooks.py     # Callbacks
│   │   │   └── websockets/
│   │   │       └── progress.py     # Real-time updates
│   │   │
│   │   ├── core/
│   │   │   ├── task_parser.py      # NLP → structured task
│   │   │   ├── task_decomposer.py  # Duży task → subtasks (używa PLANNING LLM)
│   │   │   ├── dependency_resolver.py
│   │   │   ├── agent_router.py     # Który framework/agent użyć
│   │   │   ├── cost_optimizer.py   # Decyzje cloud vs self-hosted
│   │   │   └── execution_engine.py # Orkiestracja wykonania
│   │   │
│   │   ├── adapters/
│   │   │   ├── base.py             # Abstract base adapter
│   │   │   ├── langgraph_adapter.py
│   │   │   ├── crewai_adapter.py
│   │   │   ├── autogen_adapter.py
│   │   │   └── agency_swarm_adapter.py
│   │   │
│   │   ├── llm/
│   │   │   ├── router.py           # Inteligentny routing między LLM
│   │   │   ├── planning_client.py  # Claude/GPT-4 API client
│   │   │   ├── execution_client.py # Self-hosted LLM client (OpenAI-compatible)
│   │   │   ├── cost_tracker.py     # Śledzenie kosztów
│   │   │   └── providers/
│   │   │       ├── anthropic.py
│   │   │       ├── openai.py
│   │   │       ├── runpod.py       # RunPod serverless
│   │   │       └── vllm.py         # Self-hosted vLLM
│   │   │
│   │   ├── models/
│   │   │   ├── task.py             # SQLAlchemy models
│   │   │   ├── agent.py
│   │   │   ├── execution.py
│   │   │   └── cost_log.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── task.py             # Pydantic schemas
│   │   │   ├── agent.py
│   │   │   └── execution.py
│   │   │
│   │   └── workers/
│   │       ├── task_executor.py    # Celery/ARQ worker
│   │       └── gpu_manager.py      # Start/stop GPU instances
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_decomposer.py
│       ├── test_adapters.py
│       └── test_llm_router.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── TaskInput.tsx       # Formularz nowego taska
│   │   │   ├── TaskBoard.tsx       # Kanban board
│   │   │   ├── TaskTree.tsx        # Drzewo subtasków
│   │   │   ├── AgentPanel.tsx      # Lista agentów i ich status
│   │   │   ├── ExecutionLog.tsx    # Real-time logi
│   │   │   ├── CostDashboard.tsx   # Koszty LLM
│   │   │   └── SettingsPanel.tsx   # Konfiguracja LLM providers
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useTasks.ts
│   │   │   └── useAgents.ts
│   │   ├── stores/
│   │   │   └── taskStore.ts        # Zustand
│   │   └── types/
│   │       └── index.ts
│   └── Dockerfile
│
└── docs/
    ├── architecture.md
    ├── deployment.md
    ├── cost-optimization.md
    └── adding-new-adapter.md
```

---

## 🔧 KLUCZOWE IMPLEMENTACJE

### 1. Task Decomposer (używa PLANNING LLM)

```python
# backend/app/core/task_decomposer.py

from typing import List
from pydantic import BaseModel
from app.llm.router import LLMRouter

class SubTask(BaseModel):
    id: str
    title: str
    description: str
    estimated_complexity: str  # "simple" | "medium" | "complex"
    suggested_framework: str   # "langgraph" | "crewai" | "autogen" | "agency_swarm"
    suggested_agent_role: str  # "architect" | "developer" | "reviewer" | "security" | "ui" | "ux"
    dependencies: List[str]    # IDs of tasks this depends on
    acceptance_criteria: List[str]

class TaskDecomposition(BaseModel):
    original_task: str
    architecture_overview: str
    subtasks: List[SubTask]
    execution_order: List[List[str]]  # Groups of parallel tasks
    estimated_total_cost_usd: float
    estimated_time_minutes: int

class TaskDecomposer:
    DECOMPOSITION_PROMPT = '''
    Jesteś architektem systemów AI. Rozłóż poniższe zadanie na mniejsze, wykonalne subtaski.
    
    ZASADY:
    1. Każdy subtask powinien być możliwy do wykonania przez jednego agenta w <30 min
    2. Subtaski "simple" i "medium" → self-hosted LLM (Qwen2.5-Coder)
    3. Subtaski "complex" → mogą wymagać cloud LLM do review
    4. Określ zależności między taskami
    5. Sugeruj framework na podstawie:
       - langgraph: workflow krok-po-kroku, checkpointing
       - crewai: role-based, hierarchiczna delegacja
       - autogen: dyskusja między agentami, code review
       - agency_swarm: proste narzędzia, szybkie akcje
    
    ZADANIE:
    {task}
    
    Odpowiedz w formacie JSON zgodnym z TaskDecomposition schema.
    '''
    
    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router
    
    async def decompose(self, task: str) -> TaskDecomposition:
        response = await self.llm.planning_call(
            prompt=self.DECOMPOSITION_PROMPT.format(task=task),
            response_model=TaskDecomposition,
            max_tokens=4000
        )
        return response
```

### 2. LLM Router (inteligentny wybór modelu)

```python
# backend/app/llm/router.py

from enum import Enum
from typing import Optional, Type
from pydantic import BaseModel
import httpx

class LLMTier(Enum):
    PLANNING = "planning"      # Cloud API (Claude/GPT-4)
    EXECUTION = "execution"    # Self-hosted (Qwen/DeepSeek)

class LLMRouter:
    def __init__(self, config: "LLMConfig"):
        self.config = config
        self.cost_tracker = CostTracker()
        
        # Planning tier clients
        self.planning_clients = {
            "anthropic": AnthropicClient(config.anthropic_api_key),
            "openai": OpenAIClient(config.openai_api_key),
        }
        
        # Execution tier clients (OpenAI-compatible endpoints)
        self.execution_clients = {
            "runpod": RunPodClient(config.runpod_api_key, config.runpod_endpoint),
            "vllm_local": VLLMClient(config.vllm_endpoint),  # localhost:8000
            "vastai": VastAIClient(config.vastai_config),
        }
    
    async def planning_call(
        self,
        prompt: str,
        response_model: Optional[Type[BaseModel]] = None,
        max_tokens: int = 2000,
        provider: str = "anthropic"
    ) -> BaseModel | str:
        """Wywołanie do Planning LLM (cloud) - używaj oszczędnie!"""
        client = self.planning_clients[provider]
        
        # Track cost
        input_tokens = self._estimate_tokens(prompt)
        
        response = await client.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            response_model=response_model
        )
        
        output_tokens = self._estimate_tokens(str(response))
        await self.cost_tracker.log(
            tier=LLMTier.PLANNING,
            provider=provider,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        
        return response
    
    async def execution_call(
        self,
        prompt: str,
        max_tokens: int = 4000,
        provider: str = "auto"
    ) -> str:
        """Wywołanie do Execution LLM (self-hosted) - główny workhorse"""
        
        if provider == "auto":
            provider = await self._select_best_execution_provider()
        
        client = self.execution_clients[provider]
        
        response = await client.generate(
            prompt=prompt,
            max_tokens=max_tokens
        )
        
        # Execution tier is free (self-hosted) or very cheap
        await self.cost_tracker.log(
            tier=LLMTier.EXECUTION,
            provider=provider,
            input_tokens=self._estimate_tokens(prompt),
            output_tokens=self._estimate_tokens(response),
            cost_usd=0.0  # Self-hosted = free
        )
        
        return response
    
    async def _select_best_execution_provider(self) -> str:
        """Auto-select based on availability and latency"""
        # Priority: local vLLM > RunPod > Vast.ai
        
        if await self._check_health("vllm_local"):
            return "vllm_local"
        
        if await self._check_health("runpod"):
            return "runpod"
        
        # Vast.ai as fallback, might need to spin up instance
        return "vastai"
```

### 3. RunPod Integration

```python
# backend/app/llm/providers/runpod.py

import httpx
from typing import Optional

class RunPodClient:
    """
    RunPod Serverless dla Qwen2.5-Coder-32B
    
    Setup:
    1. Deploy template: runpod/worker-vllm:stable-cuda12.1.0
    2. Model: Qwen/Qwen2.5-Coder-32B-Instruct-AWQ (quantized)
    3. GPU: RTX 4090 (24GB) - ~$0.44/hr
    """
    
    BASE_URL = "https://api.runpod.ai/v2"
    
    def __init__(self, api_key: str, endpoint_id: str):
        self.api_key = api_key
        self.endpoint_id = endpoint_id
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=120.0
        )
    
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.1
    ) -> str:
        # RunPod serverless - auto scales to 0 when idle
        response = await self.client.post(
            f"{self.BASE_URL}/{self.endpoint_id}/runsync",
            json={
                "input": {
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "stop": ["```\n\n", "</code>"]
                }
            }
        )
        response.raise_for_status()
        
        result = response.json()
        if result["status"] == "COMPLETED":
            return result["output"]["text"]
        else:
            raise RuntimeError(f"RunPod job failed: {result}")
    
    async def check_health(self) -> bool:
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/{self.endpoint_id}/health"
            )
            return response.status_code == 200
        except:
            return False
    
    async def scale_up(self, min_workers: int = 1):
        """Pre-warm workers for faster response"""
        await self.client.post(
            f"{self.BASE_URL}/{self.endpoint_id}/scale",
            json={"minWorkers": min_workers}
        )
    
    async def scale_down(self):
        """Scale to 0 to save costs"""
        await self.client.post(
            f"{self.BASE_URL}/{self.endpoint_id}/scale",
            json={"minWorkers": 0}
        )
```

### 4. Adapter Base Class

```python
# backend/app/adapters/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class AgentConfig(BaseModel):
    role: str
    goal: str
    backstory: Optional[str] = None
    tools: List[str] = []
    llm_tier: str = "execution"  # "planning" | "execution"

class TaskResult(BaseModel):
    success: bool
    output: Any
    artifacts: List[str] = []  # File paths
    logs: List[str] = []
    tokens_used: int = 0
    execution_time_seconds: float = 0

class BaseAdapter(ABC):
    """Abstrakcyjna klasa bazowa dla wszystkich adapterów frameworków"""
    
    def __init__(self, llm_router: "LLMRouter"):
        self.llm = llm_router
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nazwa frameworka"""
        pass
    
    @property
    @abstractmethod
    def strengths(self) -> List[str]:
        """Lista mocnych stron - używane do routingu"""
        pass
    
    @abstractmethod
    async def create_agent(self, config: AgentConfig) -> Any:
        """Tworzy agenta w danym frameworku"""
        pass
    
    @abstractmethod
    async def execute_task(
        self,
        agent: Any,
        task_description: str,
        context: Optional[Dict] = None
    ) -> TaskResult:
        """Wykonuje zadanie przez agenta"""
        pass
    
    @abstractmethod
    async def create_workflow(
        self,
        agents: List[Any],
        task_descriptions: List[str],
        dependencies: Dict[str, List[str]]
    ) -> Any:
        """Tworzy workflow z wielu agentów"""
        pass
```

### 5. CrewAI Adapter Example

```python
# backend/app/adapters/crewai_adapter.py

from crewai import Agent, Task, Crew, Process
from app.adapters.base import BaseAdapter, AgentConfig, TaskResult
from app.llm.router import LLMRouter

class CrewAIAdapter(BaseAdapter):
    
    @property
    def name(self) -> str:
        return "crewai"
    
    @property
    def strengths(self) -> List[str]:
        return [
            "role-based collaboration",
            "hierarchical delegation",
            "task pipeline",
            "production-ready"
        ]
    
    async def create_agent(self, config: AgentConfig) -> Agent:
        # CrewAI używa własnego LLM wrappera
        # Ale możemy przekierować na nasz execution tier
        
        return Agent(
            role=config.role,
            goal=config.goal,
            backstory=config.backstory or f"Expert {config.role}",
            tools=self._load_tools(config.tools),
            llm=self._create_llm_wrapper(config.llm_tier),
            verbose=True
        )
    
    def _create_llm_wrapper(self, tier: str):
        """Wrapper który kieruje CrewAI do naszego LLM Router"""
        from langchain.llms.base import LLM
        
        class RouterLLM(LLM):
            def __init__(self, router: LLMRouter, tier: str):
                self.router = router
                self.tier = tier
            
            def _call(self, prompt: str, **kwargs) -> str:
                import asyncio
                if self.tier == "planning":
                    return asyncio.run(self.router.planning_call(prompt))
                else:
                    return asyncio.run(self.router.execution_call(prompt))
            
            @property
            def _llm_type(self) -> str:
                return "router"
        
        return RouterLLM(self.llm, tier)
    
    async def execute_task(
        self,
        agent: Agent,
        task_description: str,
        context: Optional[Dict] = None
    ) -> TaskResult:
        import time
        start = time.time()
        
        task = Task(
            description=task_description,
            agent=agent,
            expected_output="Completed task with all deliverables"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        try:
            result = crew.kickoff()
            return TaskResult(
                success=True,
                output=result,
                execution_time_seconds=time.time() - start
            )
        except Exception as e:
            return TaskResult(
                success=False,
                output=str(e),
                logs=[f"Error: {e}"],
                execution_time_seconds=time.time() - start
            )
```

---

## 🐳 DOCKER & DEPLOYMENT

### docker-compose.yml (Development)

```yaml
version: '3.8'

services:
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/orchestrator
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - RUNPOD_API_KEY=${RUNPOD_API_KEY}
      - RUNPOD_ENDPOINT_ID=${RUNPOD_ENDPOINT_ID}
      - VLLM_ENDPOINT=http://host.docker.internal:8080  # Local vLLM
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis
    command: uvicorn app.main:app --reload --host 0.0.0.0
  
  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.worker
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/orchestrator
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - RUNPOD_API_KEY=${RUNPOD_API_KEY}
    depends_on:
      - db
      - redis
    command: arq app.workers.task_executor.WorkerSettings
  
  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
    environment:
      - VITE_API_URL=http://localhost:8000
  
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=orchestrator
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Dockerfile.api

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system deps for ML libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[dev]"

# Copy source
COPY . .

# Run
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ☁️ INFRASTRUCTURE (Terraform)

### RunPod GPU Setup

```hcl
# infrastructure/terraform/runpod.tf

terraform {
  required_providers {
    runpod = {
      source = "runpod/runpod"
    }
  }
}

provider "runpod" {
  api_key = var.runpod_api_key
}

# Serverless Endpoint dla Qwen2.5-Coder-32B
resource "runpod_endpoint" "qwen_coder" {
  name = "qwen-coder-32b"
  
  template_id = "runpod/worker-vllm:stable-cuda12.1.0"
  
  gpu_ids = ["NVIDIA RTX 4090"]  # ~$0.44/hr
  
  env = {
    MODEL_NAME = "Qwen/Qwen2.5-Coder-32B-Instruct-AWQ"
    MAX_MODEL_LEN = "32768"
    QUANTIZATION = "awq"
  }
  
  scaling_config {
    min_workers     = 0      # Scale to zero when idle!
    max_workers     = 3
    idle_timeout    = 60     # Seconds before scale down
  }
  
  # Webhook for completion notifications
  webhook_url = "${var.api_base_url}/webhooks/runpod"
}

output "runpod_endpoint_id" {
  value = runpod_endpoint.qwen_coder.id
}
```

### Hetzner VPS dla API (tani)

```hcl
# infrastructure/terraform/hetzner.tf

provider "hcloud" {
  token = var.hetzner_api_token
}

# API Server - CX31 (~€10/mo)
resource "hcloud_server" "api" {
  name        = "agent-orchestrator-api"
  image       = "ubuntu-22.04"
  server_type = "cx31"  # 2 vCPU, 8GB RAM
  location    = "fsn1"
  
  ssh_keys = [hcloud_ssh_key.main.id]
  
  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io docker-compose-plugin
    systemctl enable docker
    
    # Setup app
    mkdir -p /opt/orchestrator
    # ... clone repo, setup env, docker compose up -d
  EOF
}

# Managed PostgreSQL - €15/mo
resource "hcloud_managed_database" "postgres" {
  name         = "orchestrator-db"
  database_type = "postgres"
  server_type  = "cx11"
}

output "api_ip" {
  value = hcloud_server.api.ipv4_address
}
```

---

## 💰 COST OPTIMIZATION STRATEGY

### Automatic GPU Scaling

```python
# backend/app/workers/gpu_manager.py

import asyncio
from datetime import datetime, timedelta
from app.llm.providers.runpod import RunPodClient

class GPUManager:
    """
    Zarządza GPU instances aby minimalizować koszty:
    - Scale to 0 gdy brak aktywności
    - Pre-warm przed spodziewanym ruchem
    - Track usage i koszty
    """
    
    def __init__(self, runpod: RunPodClient, redis: "Redis"):
        self.runpod = runpod
        self.redis = redis
        self.IDLE_THRESHOLD_MINUTES = 5
        self.COST_PER_HOUR = 0.44  # RTX 4090
    
    async def ensure_capacity(self, expected_tasks: int):
        """Pre-warm workers based on queue size"""
        if expected_tasks > 0:
            workers_needed = min(expected_tasks, 3)
            await self.runpod.scale_up(workers_needed)
            await self.redis.set("gpu_last_activity", datetime.utcnow().isoformat())
    
    async def check_idle_and_scale_down(self):
        """Background task - scale down if idle"""
        last_activity = await self.redis.get("gpu_last_activity")
        if last_activity:
            last_dt = datetime.fromisoformat(last_activity)
            if datetime.utcnow() - last_dt > timedelta(minutes=self.IDLE_THRESHOLD_MINUTES):
                await self.runpod.scale_down()
                print("Scaled GPU to 0 due to inactivity")
    
    async def get_daily_cost(self) -> float:
        """Calculate today's GPU costs"""
        # Track in Redis sorted set: gpu_usage:{date} -> seconds
        today = datetime.utcnow().strftime("%Y-%m-%d")
        seconds_used = await self.redis.get(f"gpu_usage:{today}") or 0
        hours_used = int(seconds_used) / 3600
        return hours_used * self.COST_PER_HOUR
```

### Cost-Aware Task Router

```python
# backend/app/core/cost_optimizer.py

class CostOptimizer:
    """
    Decyduje który tier LLM użyć na podstawie:
    - Złożoności taska
    - Budżetu dziennego
    - Aktualnych kosztów
    """
    
    DAILY_CLOUD_BUDGET_USD = 5.0  # Max $5/day na Cloud LLM
    
    async def should_use_planning_tier(
        self,
        task_type: str,
        complexity: str,
        current_daily_cost: float
    ) -> bool:
        """
        Zwraca True jeśli powinniśmy użyć Planning tier (Cloud LLM)
        """
        # Zawsze używaj Planning dla:
        if task_type in ["decomposition", "architecture", "final_review"]:
            return True
        
        # Sprawdź budżet
        if current_daily_cost >= self.DAILY_CLOUD_BUDGET_USD:
            return False  # Budżet wyczerpany - fallback to self-hosted
        
        # Complex tasks mogą używać Planning jeśli jest budżet
        if complexity == "complex" and current_daily_cost < self.DAILY_CLOUD_BUDGET_USD * 0.8:
            return True
        
        return False
```

---

## 🖥️ FRONTEND COMPONENTS

### TaskInput.tsx

```tsx
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { api } from '../api';

export function TaskInput() {
  const [task, setTask] = useState('');
  
  const decomposeMutation = useMutation({
    mutationFn: (taskDescription: string) => 
      api.post('/tasks/decompose', { description: taskDescription }),
    onSuccess: (data) => {
      // Navigate to task board with decomposed tasks
    }
  });
  
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">🚀 Nowe zadanie</h1>
      
      <textarea
        value={task}
        onChange={(e) => setTask(e.target.value)}
        placeholder="Opisz co chcesz zbudować... np. 'Zbuduj REST API do zarządzania użytkownikami z autentykacją JWT'"
        className="w-full h-40 p-4 border rounded-lg resize-none"
      />
      
      <div className="mt-4 flex gap-4">
        <button
          onClick={() => decomposeMutation.mutate(task)}
          disabled={!task.trim() || decomposeMutation.isPending}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {decomposeMutation.isPending ? '🔄 Analizuję...' : '📋 Rozłóż na subtaski'}
        </button>
        
        <button
          onClick={() => {/* direct execute */}}
          className="px-6 py-2 border rounded-lg hover:bg-gray-50"
        >
          ⚡ Wykonaj bez rozkładania
        </button>
      </div>
      
      {decomposeMutation.isPending && (
        <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
          <p className="text-sm text-yellow-800">
            🧠 Używam Claude Opus do analizy i rozbicia zadania...
            <br />
            <span className="text-xs">Szacowany koszt: ~$0.05</span>
          </p>
        </div>
      )}
    </div>
  );
}
```

### CostDashboard.tsx

```tsx
import { useQuery } from '@tanstack/react-query';

export function CostDashboard() {
  const { data: costs } = useQuery({
    queryKey: ['costs'],
    queryFn: () => api.get('/costs/summary'),
    refetchInterval: 30000
  });
  
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="font-bold mb-4">💰 Koszty LLM</h2>
      
      <div className="grid grid-cols-3 gap-4">
        <div className="p-3 bg-blue-50 rounded">
          <p className="text-xs text-gray-500">Dzisiaj (Cloud)</p>
          <p className="text-xl font-bold">${costs?.today_cloud?.toFixed(2) || '0.00'}</p>
          <p className="text-xs text-gray-400">Limit: $5.00</p>
        </div>
        
        <div className="p-3 bg-green-50 rounded">
          <p className="text-xs text-gray-500">Dzisiaj (Self-hosted)</p>
          <p className="text-xl font-bold">${costs?.today_gpu?.toFixed(2) || '0.00'}</p>
          <p className="text-xs text-gray-400">GPU time: {costs?.gpu_hours?.toFixed(1)}h</p>
        </div>
        
        <div className="p-3 bg-purple-50 rounded">
          <p className="text-xs text-gray-500">Ten miesiąc</p>
          <p className="text-xl font-bold">${costs?.month_total?.toFixed(2) || '0.00'}</p>
        </div>
      </div>
      
      <div className="mt-4">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Cloud budget</span>
          <span>{((costs?.today_cloud || 0) / 5 * 100).toFixed(0)}%</span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-blue-500 transition-all"
            style={{ width: `${Math.min(100, (costs?.today_cloud || 0) / 5 * 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
}
```

---

## 🚀 DEPLOYMENT CHECKLIST

### Faza 1: Local Development
- [ ] Setup docker-compose.yml
- [ ] Zaimplementuj core: TaskDecomposer, LLMRouter
- [ ] Zaimplementuj 2 adaptery (CrewAI + LangGraph)
- [ ] Basic UI z TaskInput i TaskBoard
- [ ] Integracja z RunPod Serverless (Qwen2.5-Coder)

### Faza 2: Staging
- [ ] Deploy API na Hetzner VPS (CX31)
- [ ] Setup PostgreSQL (managed lub self-hosted)
- [ ] Setup Redis
- [ ] Configure RunPod endpoint
- [ ] SSL via Caddy/nginx

### Faza 3: Production
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Alerting na koszty i błędy
- [ ] Backup strategy dla DB
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Load testing

---

## 📊 SZACOWANE KOSZTY MIESIĘCZNE

| Komponent | Koszt | Uwagi |
|-----------|-------|-------|
| Hetzner VPS (API) | €10 | CX31 - 2vCPU, 8GB |
| Hetzner PostgreSQL | €15 | Managed, backups |
| RunPod GPU | ~$50-100 | Zależy od użycia, scale-to-zero |
| Cloud LLM (Claude/GPT) | ~$30-50 | Planning tier only |
| Domain + SSL | ~$15/yr | Cloudflare free tier |
| **TOTAL** | **~$100-180/mo** | Przy umiarkowanym użyciu |

vs. Gdyby wszystko szło przez Cloud LLM: **$500-1000+/mo**

---

## ⚠️ POTENCJALNE PROBLEMY I ROZWIĄZANIA

| Problem | Rozwiązanie |
|---------|-------------|
| Cold start RunPod (~30s) | Pre-warm przed spodziewanym ruchem, queue tasks |
| Context limit self-hosted | Chunk large codebases, use embeddings for retrieval |
| Framework conflicts | Izoluj w osobnych procesach/kontenerach |
| Rate limits Cloud API | Exponential backoff, queue z priority |
| GPU availability Vast.ai | Fallback do RunPod, multiple regions |

---

## 🎯 PIERWSZE KROKI

1. **Sklonuj repo i setup environment**
2. **Zaimplementuj `LLMRouter` z mockami** - testuj flow bez prawdziwych API
3. **Zaimplementuj `TaskDecomposer`** - to serce systemu
4. **Dodaj jeden adapter (CrewAI)** - najprostszy do integracji
5. **Basic UI** - TaskInput → TaskBoard
6. **Integracja RunPod** - deploy Qwen2.5-Coder endpoint
7. **Iteruj i dodawaj kolejne adaptery**

---

## 📝 NOTATKI DLA CLAUDE CODE

- Używaj **Python 3.11+** z **type hints** wszędzie
- **Pydantic v2** dla wszystkich schemas
- **FastAPI** z **async/await** konsekwentnie
- **pytest-asyncio** dla testów
- Każdy adapter powinien mieć **własne testy integracyjne**
- **Loguj wszystko** - szczególnie koszty LLM i czasy wykonania
- **Feature flags** dla nowych adapterów (łatwe włączanie/wyłączanie)
- **Health checks** dla wszystkich zewnętrznych serwisów


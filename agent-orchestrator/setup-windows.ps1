# Agent Orchestrator - Setup Script dla Windows
# Alternatywa dla Makefile na Windows

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("install", "docker-up", "docker-down", "migrate", "backend", "frontend", "test", "lint", "clean")]
    [string]$Command = "help"
)

$ErrorActionPreference = "Stop"

function Show-Help {
    Write-Host @"
Agent Orchestrator - PowerShell Setup Script

Użycie:
    .\setup-windows.ps1 <command>

Dostępne komendy:
    install      - Instalacja zależności (backend + frontend)
    docker-up    - Uruchom PostgreSQL i Redis w Docker
    docker-down  - Zatrzymaj kontenery Docker
    migrate      - Wykonaj migracje bazy danych
    backend      - Uruchom backend (uvicorn)
    frontend     - Uruchom frontend (npm run dev)
    test         - Uruchom testy backend
    lint         - Sprawdź kod (ruff + eslint)
    clean        - Wyczyść cache i pliki tymczasowe

Przykłady:
    .\setup-windows.ps1 install
    .\setup-windows.ps1 docker-up
    .\setup-windows.ps1 migrate
    .\setup-windows.ps1 backend
"@
}

function Install-Dependencies {
    Write-Host "📦 Instalacja zależności..." -ForegroundColor Cyan
    
    # Backend
    Write-Host "`n🔧 Backend..." -ForegroundColor Yellow
    Push-Location backend
    if (-not (Test-Path ".venv")) {
        Write-Host "Tworzenie virtual environment..."
        python -m venv .venv
    }
    & .\.venv\Scripts\Activate.ps1
    pip install -e ".[dev]"
    
    # Sprawdź czy langchain jest zainstalowany (wymagany przez CrewAI)
    $langchainInstalled = & .\.venv\Scripts\pip.exe list | Select-String "langchain"
    if (-not $langchainInstalled) {
        Write-Host "📦 Instalowanie langchain (wymagane przez CrewAI)..." -ForegroundColor Yellow
        & .\.venv\Scripts\pip.exe install langchain langchain-core
    }
    
    Pop-Location
    
    # Frontend
    Write-Host "`n🔧 Frontend..." -ForegroundColor Yellow
    Push-Location frontend
    npm install
    Pop-Location
    
    Write-Host "`n✅ Zależności zainstalowane!" -ForegroundColor Green
}

function Start-Docker {
    Write-Host "🐳 Uruchamianie Docker Compose..." -ForegroundColor Cyan
    
    # Sprawdź czy Docker Desktop jest uruchomiony
    try {
        $null = docker info 2>&1
    } catch {
        Write-Host "❌ Docker Desktop nie jest uruchomiony!" -ForegroundColor Red
        Write-Host "`nRozwiązanie:" -ForegroundColor Yellow
        Write-Host "1. Uruchom Docker Desktop z menu Start" -ForegroundColor White
        Write-Host "2. Poczekaj aż Docker Desktop się w pełni uruchomi (ikona w system tray)" -ForegroundColor White
        Write-Host "3. Spróbuj ponownie: .\setup-windows.ps1 docker-up" -ForegroundColor White
        return
    }
    
    # Sprawdź czy docker-compose jest dostępne
    if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Host "⚠️  docker-compose nie znalezione, próbuję 'docker compose'..." -ForegroundColor Yellow
        $composeCmd = "docker compose"
    } else {
        $composeCmd = "docker-compose"
    }
    
    # Uruchom docker-compose
    $result = & $composeCmd.Split(' ') up -d db redis 2>&1
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -ne 0) {
        Write-Host "❌ Błąd uruchamiania Docker Compose!" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
        Write-Host "`nSprawdź:" -ForegroundColor Yellow
        Write-Host "- Czy Docker Desktop jest uruchomiony?" -ForegroundColor White
        Write-Host "- Czy masz uprawnienia administratora?" -ForegroundColor White
        Write-Host "- Sprawdź logi: docker-compose logs" -ForegroundColor White
        return
    }
    
    Write-Host "✅ Docker uruchomiony!" -ForegroundColor Green
    Write-Host "Sprawdź status: docker-compose ps" -ForegroundColor Gray
}

function Stop-Docker {
    Write-Host "🐳 Zatrzymywanie Docker Compose..." -ForegroundColor Cyan
    
    # Sprawdź czy docker-compose jest dostępne
    if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        $composeCmd = "docker compose"
    } else {
        $composeCmd = "docker-compose"
    }
    
    & $composeCmd.Split(' ') down
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker zatrzymany!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Nie udało się zatrzymać kontenerów" -ForegroundColor Yellow
    }
}

function Invoke-Migrate {
    Write-Host "🗄️  Wykonywanie migracji..." -ForegroundColor Cyan
    Push-Location backend
    if (Test-Path ".venv") {
        & .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host "⚠️  Virtual environment nie znalezione. Uruchom najpierw: .\setup-windows.ps1 install" -ForegroundColor Yellow
        Pop-Location
        return
    }
    
    # Sprawdź czy psycopg2-binary jest zainstalowany (wymagany dla migracji)
    $psycopg2Installed = & .\.venv\Scripts\pip.exe list | Select-String "psycopg2-binary"
    if (-not $psycopg2Installed) {
        Write-Host "📦 Instalowanie psycopg2-binary (wymagane dla migracji)..." -ForegroundColor Yellow
        & .\.venv\Scripts\pip.exe install psycopg2-binary
    }
    
    alembic upgrade head
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Migracje wykonane!" -ForegroundColor Green
    } else {
        Write-Host "❌ Błąd podczas migracji!" -ForegroundColor Red
    }
    Pop-Location
}

function Start-Backend {
    Write-Host "🚀 Uruchamianie backend..." -ForegroundColor Cyan
    Push-Location backend
    if (Test-Path ".venv") {
        & .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host "⚠️  Virtual environment nie znalezione. Uruchom najpierw: .\setup-windows.ps1 install" -ForegroundColor Yellow
        Pop-Location
        return
    }
    Write-Host "Backend dostępny na: http://localhost:8000" -ForegroundColor Green
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
    uvicorn app.main:app --reload --port 8000
}

function Start-Frontend {
    Write-Host "🚀 Uruchamianie frontend..." -ForegroundColor Cyan
    Push-Location frontend
    Write-Host "Frontend dostępny na: http://localhost:3000" -ForegroundColor Green
    npm run dev
}

function Invoke-Test {
    Write-Host "🧪 Uruchamianie testów..." -ForegroundColor Cyan
    Push-Location backend
    if (Test-Path ".venv") {
        & .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host "⚠️  Virtual environment nie znalezione. Uruchom najpierw: .\setup-windows.ps1 install" -ForegroundColor Yellow
        Pop-Location
        return
    }
    pytest -v --cov=app
    Pop-Location
}

function Invoke-Lint {
    Write-Host "🔍 Sprawdzanie kodu..." -ForegroundColor Cyan
    
    # Backend
    Write-Host "`n🔧 Backend (ruff)..." -ForegroundColor Yellow
    Push-Location backend
    if (Test-Path ".venv") {
        & .\.venv\Scripts\Activate.ps1
        ruff check app tests
    }
    Pop-Location
    
    # Frontend
    Write-Host "`n🔧 Frontend (eslint)..." -ForegroundColor Yellow
    Push-Location frontend
    npm run lint
    Pop-Location
    
    Write-Host "`n✅ Linting zakończony!" -ForegroundColor Green
}

function Clear-Cache {
    Write-Host "🧹 Czyszczenie cache..." -ForegroundColor Cyan
    
    # Python cache
    Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse -Force | Remove-Item -Force -Recurse
    Get-ChildItem -Path . -Include .pytest_cache -Recurse -Force | Remove-Item -Force -Recurse
    
    # Node modules (opcjonalnie - zakomentuj jeśli chcesz zachować)
    # Get-ChildItem -Path . -Include node_modules -Recurse -Force | Remove-Item -Force -Recurse
    
    Write-Host "✅ Cache wyczyszczony!" -ForegroundColor Green
}

# Main
switch ($Command) {
    "install" { Install-Dependencies }
    "docker-up" { Start-Docker }
    "docker-down" { Stop-Docker }
    "migrate" { Invoke-Migrate }
    "backend" { Start-Backend }
    "frontend" { Start-Frontend }
    "test" { Invoke-Test }
    "lint" { Invoke-Lint }
    "clean" { Clear-Cache }
    default { Show-Help }
}


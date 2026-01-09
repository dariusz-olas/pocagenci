# Generator API Key dla Agent Orchestrator
# Generuje bezpieczny klucz API o długości 32+ znaków

param(
    [Parameter(Mandatory=$false)]
    [int]$Length = 32
)

if ($Length -lt 32) {
    Write-Host "⚠️  Długość klucza musi być minimum 32 znaki. Ustawiam na 32." -ForegroundColor Yellow
    $Length = 32
}

# Generuj losowy klucz z liter i cyfr
$chars = (48..57) + (65..90) + (97..122)  # 0-9, A-Z, a-z
$apiKey = -join ((1..$Length) | ForEach-Object { 
    $chars | Get-Random 
})

Write-Host "`n🔑 Wygenerowany API Key:" -ForegroundColor Cyan
Write-Host $apiKey -ForegroundColor Green
Write-Host "`nDodaj do backend\.env:" -ForegroundColor Yellow
Write-Host "API_KEY=$apiKey" -ForegroundColor White
Write-Host ""


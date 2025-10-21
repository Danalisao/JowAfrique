# Script PowerShell pour démarrer l'API JowAfrique
param(
    [switch]$Test,
    [switch]$Help
)

if ($Help) {
    Write-Host "🍽️  JowAfrique API Starter" -ForegroundColor Green
    Write-Host "Usage: .\start_api.ps1 [-Test] [-Help]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Test    Teste l'API après le démarrage"
    Write-Host "  -Help    Affiche cette aide"
    exit 0
}

Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "🍽️  JowAfrique API Starter" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Cyan

# Vérifier Python
Write-Host "🔍 Vérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python trouvé: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python non trouvé. Installez Python 3.8+ depuis https://python.org" -ForegroundColor Red
    exit 1
}

# Vérifier les dépendances
Write-Host "🔍 Vérification des dépendances..." -ForegroundColor Yellow
try {
    python -c "import flask, flask_cors" 2>$null
    Write-Host "✅ Dépendances installées" -ForegroundColor Green
} catch {
    Write-Host "❌ Dépendances manquantes. Installation..." -ForegroundColor Yellow
    pip install flask flask-cors
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Échec de l'installation des dépendances" -ForegroundColor Red
        exit 1
    }
}

# Vérifier la base de données
Write-Host "🔍 Vérification de la base de données..." -ForegroundColor Yellow
if (Test-Path "backend\jowafrique.db") {
    Write-Host "✅ Base de données trouvée" -ForegroundColor Green
} else {
    Write-Host "⚠️  Base de données non trouvée, elle sera créée automatiquement" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Informations de l'API:" -ForegroundColor Cyan
Write-Host "   URL: http://localhost:5000" -ForegroundColor White
Write-Host "   Health Check: http://localhost:5000/api/health" -ForegroundColor White
Write-Host "   Documentation: http://localhost:5000/api/" -ForegroundColor White
Write-Host ""
Write-Host "💡 Appuyez sur Ctrl+C pour arrêter l'API" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Cyan

# Démarrer l'API
Write-Host "🚀 Démarrage de l'API..." -ForegroundColor Green
Set-Location backend

try {
    if ($Test) {
        # Démarrer l'API en arrière-plan pour les tests
        $job = Start-Job -ScriptBlock { python api.py }
        
        # Attendre que l'API démarre
        Write-Host "⏳ Attente du démarrage de l'API..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # Tester l'API
        Write-Host "🧪 Test de l'API..." -ForegroundColor Yellow
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -TimeoutSec 10
            Write-Host "✅ API opérationnelle: $($response.status)" -ForegroundColor Green
            Write-Host "📊 Version: $($response.version)" -ForegroundColor Green
        } catch {
            Write-Host "❌ Erreur lors du test de l'API: $($_.Exception.Message)" -ForegroundColor Red
        }
        
        # Arrêter le job
        Stop-Job $job
        Remove-Job $job
    } else {
        # Démarrer l'API normalement
        python api.py
    }
} catch {
    Write-Host "❌ Erreur lors du démarrage: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    Set-Location ..
}

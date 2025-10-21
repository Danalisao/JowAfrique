# Script de démarrage en production (Windows)
Write-Host "🚀 Starting JowAfrique in production mode..." -ForegroundColor Green

# Vérifier les variables d'environnement
if (-not (Test-Path "backend\.env")) {
    Write-Host "❌ Erreur: Fichier .env manquant dans backend\" -ForegroundColor Red
    Write-Host "📝 Copiez backend\.env.example vers backend\.env et configurez-le" -ForegroundColor Yellow
    exit 1
}

# Vérifier la clé Gemini
$envContent = Get-Content "backend\.env" -Raw
if ($envContent -match "your-gemini-api-key-here") {
    Write-Host "⚠️  Attention: Clé Gemini API non configurée" -ForegroundColor Yellow
    Write-Host "📝 Configurez GEMINI_API_KEY dans backend\.env" -ForegroundColor Yellow
}

# Démarrer le backend
Write-Host "🐍 Starting backend API..." -ForegroundColor Yellow
Set-Location backend
Start-Process python -ArgumentList "api.py" -WindowStyle Hidden
Set-Location ..

# Attendre que le backend soit prêt
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Vérifier que le backend fonctionne
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/plans" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Backend API started successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend API failed to start" -ForegroundColor Red
    exit 1
}

# Démarrer le frontend
Write-Host "⚛️  Starting frontend..." -ForegroundColor Yellow
Set-Location frontend
Start-Process npm -ArgumentList "start" -WindowStyle Hidden
Set-Location ..

Write-Host "✅ JowAfrique is running in production mode!" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔌 Backend API: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pour arrêter l'application, fermez cette fenêtre ou utilisez Ctrl+C" -ForegroundColor Yellow

# Attendre une entrée utilisateur
Read-Host "Appuyez sur Entrée pour arrêter l'application"

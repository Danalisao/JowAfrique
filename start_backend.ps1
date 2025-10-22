# Script de démarrage du backend JowAfrique
Write-Host "🚀 Démarrage du backend JowAfrique..." -ForegroundColor Green

# Vérifier que Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Aller dans le répertoire backend
Set-Location "backend"

# Vérifier que les dépendances sont installées
if (!(Test-Path "requirements.txt")) {
    Write-Host "❌ Fichier requirements.txt non trouvé" -ForegroundColor Red
    exit 1
}

# Installer les dépendances si nécessaire
Write-Host "📦 Vérification des dépendances..." -ForegroundColor Yellow
pip install -r requirements.txt

# Démarrer l'API
Write-Host "🔥 Démarrage de l'API sur http://localhost:5000" -ForegroundColor Cyan
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🛑 Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow
Write-Host ""

python api.py

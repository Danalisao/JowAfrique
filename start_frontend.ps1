# Script de démarrage du frontend JowAfrique
Write-Host "🚀 Démarrage du frontend JowAfrique..." -ForegroundColor Green

# Aller dans le répertoire frontend
Set-Location "frontend"

# Vérifier que Node.js est installé
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js détecté: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Installer les dépendances si nécessaire
if (!(Test-Path "node_modules")) {
    Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
    npm install
}

# Démarrer le serveur de développement
Write-Host "🔥 Démarrage du serveur de développement sur http://localhost:3000" -ForegroundColor Cyan
Write-Host "🛑 Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow
Write-Host ""

npm run dev

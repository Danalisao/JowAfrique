# Script de build pour JowAfrique (Windows)
Write-Host "🏗️  Building JowAfrique for production..." -ForegroundColor Green

# Vérifier que nous sommes dans le bon répertoire
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "❌ Erreur: Ce script doit être exécuté depuis la racine du projet" -ForegroundColor Red
    exit 1
}

# Build du frontend
Write-Host "📦 Building frontend..." -ForegroundColor Yellow
Set-Location frontend
npm ci --only=production
npm run build
Set-Location ..

# Build du backend
Write-Host "🐍 Preparing backend..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt
Set-Location ..

# Créer les répertoires nécessaires
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "backend\backups" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# Initialiser la base de données
Write-Host "🗄️  Initializing database..." -ForegroundColor Yellow
Set-Location backend
python -c "
from database import DatabaseManager
from scripts.init_cameroon_recipes import init_cameroon_recipes
db = DatabaseManager('jowafrique.db')
init_cameroon_recipes(db)
print('✅ Database initialized with Cameroonian recipes')
"
Set-Location ..

Write-Host "✅ Build completed successfully!" -ForegroundColor Green
Write-Host "🚀 Ready for production deployment" -ForegroundColor Green

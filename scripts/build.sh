#!/bin/bash

# Script de build pour JowAfrique
echo "🏗️  Building JowAfrique for production..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis la racine du projet"
    exit 1
fi

# Build du frontend
echo "📦 Building frontend..."
cd frontend
npm ci --only=production
npm run build
cd ..

# Build du backend
echo "🐍 Preparing backend..."
cd backend
pip install -r requirements.txt
cd ..

# Créer les répertoires nécessaires
echo "📁 Creating necessary directories..."
mkdir -p backend/backups
mkdir -p logs

# Initialiser la base de données
echo "🗄️  Initializing database..."
cd backend
python -c "
from database import DatabaseManager
from scripts.init_cameroon_recipes import init_cameroon_recipes
db = DatabaseManager('jowafrique.db')
init_cameroon_recipes(db)
print('✅ Database initialized with Cameroonian recipes')
"
cd ..

echo "✅ Build completed successfully!"
echo "🚀 Ready for production deployment"

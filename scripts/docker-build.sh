#!/bin/bash

# Script de build Docker pour JowAfrique
echo "🐳 Building JowAfrique with Docker..."

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    exit 1
fi

# Build des images Docker
echo "🏗️  Building Docker images..."
docker-compose build

# Démarrer les services
echo "🚀 Starting services..."
docker-compose up -d

# Attendre que les services soient prêts
echo "⏳ Waiting for services to start..."
sleep 10

# Vérifier le statut des services
echo "📊 Service status:"
docker-compose ps

# Vérifier la connectivité
if curl -s http://localhost:5000/api/plans > /dev/null; then
    echo "✅ Backend API is healthy"
else
    echo "❌ Backend API is not responding"
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend is not responding"
fi

echo ""
echo "✅ JowAfrique is running with Docker!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:5000"
echo ""
echo "Pour arrêter: docker-compose down"

#!/bin/bash

# Script de démarrage en production
echo "🚀 Starting JowAfrique in production mode..."

# Vérifier les variables d'environnement
if [ ! -f "backend/.env" ]; then
    echo "❌ Erreur: Fichier .env manquant dans backend/"
    echo "📝 Copiez backend/.env.example vers backend/.env et configurez-le"
    exit 1
fi

# Vérifier la clé Gemini
if grep -q "your-gemini-api-key-here" backend/.env; then
    echo "⚠️  Attention: Clé Gemini API non configurée"
    echo "📝 Configurez GEMINI_API_KEY dans backend/.env"
fi

# Démarrer le backend
echo "🐍 Starting backend API..."
cd backend
python api.py &
BACKEND_PID=$!
cd ..

# Attendre que le backend soit prêt
echo "⏳ Waiting for backend to start..."
sleep 5

# Vérifier que le backend fonctionne
if curl -s http://localhost:5000/api/plans > /dev/null; then
    echo "✅ Backend API started successfully"
else
    echo "❌ Backend API failed to start"
    kill $BACKEND_PID
    exit 1
fi

# Démarrer le frontend
echo "⚛️  Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ JowAfrique is running in production mode!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:5000"
echo ""
echo "Pour arrêter l'application, utilisez Ctrl+C"

# Fonction de nettoyage
cleanup() {
    echo "🛑 Stopping JowAfrique..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT SIGTERM

# Attendre que les processus se terminent
wait

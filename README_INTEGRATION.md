# 🔗 Intégration Frontend-Backend JowAfrique

## 🚀 Démarrage Rapide

### Option 1: Script automatique (Recommandé)

#### Windows (PowerShell)
```powershell
.\start_dev.ps1
```

#### Linux/Mac (Python)
```bash
python start_dev.py
```

### Option 2: Démarrage manuel

#### 1. Backend API (Port 5000)
```bash
cd backend
python api.py
```

#### 2. Frontend Next.js (Port 3000)
```bash
cd frontend
npm install
npm run dev
```

## 📡 Endpoints API Disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/meals` | GET | Récupérer tous les repas |
| `/api/current-meal` | GET | Repas en cours de préparation |
| `/api/meals/{id}` | PUT | Mettre à jour un repas |
| `/api/meals/{id}/favorite` | POST | Ajouter aux favoris |
| `/api/plans` | GET/POST | Plans hebdomadaires |
| `/api/plans/{id}` | DELETE | Supprimer un plan |
| `/api/plans/{id}/meals` | GET/POST | Repas d'un plan |
| `/api/plans/{id}/shopping-list` | GET | Liste de courses |
| `/api/favorites` | GET | Recettes favorites |
| `/api/statistics` | GET | Statistiques utilisateur |

## 🔄 Flux de Données

```
Frontend Next.js (3000) ←→ Backend Flask (5000) ←→ SQLite Database
```

### Frontend
- **React Components** - Interface utilisateur
- **API Calls** - Communication avec le backend
- **State Management** - Gestion des données locales
- **PWA Ready** - Installation mobile

### Backend
- **Flask API** - Endpoints REST
- **SQLite Database** - Stockage des données
- **CORS Enabled** - Communication cross-origin
- **JSON Responses** - Format standardisé

## 📱 Pages Frontend

1. **MainPage** - Accueil avec repas du jour
2. **ProgressPage** - Suivi de préparation
3. **FavoritesPage** - Recettes favorites
4. **SettingsPage** - Paramètres et stats
5. **CartPage** - Liste de courses

## 🛠️ Configuration

### Variables d'Environnement
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:5000

# Backend (dans api_endpoints.py)
DB_PATH=jowafrique.db
```

## 🔧 Développement

### Ajouter un Nouvel Endpoint
1. Modifier `backend/api.py`
2. Ajouter la route Flask
3. Tester avec Postman/curl
4. Intégrer dans le frontend

### Ajouter une Nouvelle Page
1. Créer le composant dans `frontend/src/components/`
2. Ajouter la route dans `frontend/src/app/page.tsx`
3. Mettre à jour la navigation

## 🐛 Debug

### Problèmes Courants
- **CORS Error** - Vérifier que Flask-CORS est installé
- **Connection Refused** - Vérifier que l'API est démarrée sur le port 5000
- **Database Error** - Vérifier que `jowafrique.db` existe

### Logs
```bash
# Backend logs
python api.py

# Frontend logs
cd frontend && npm run dev
```

## 📦 Production

### Build Frontend
```bash
cd frontend
npm run build
npm start
```

### Deploy Backend
```bash
# Avec Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

## 🎯 Prochaines Étapes

1. **Authentification** - Système de login
2. **Real-time** - WebSockets pour les notifications
3. **Offline** - Cache local avec Service Worker
4. **Push Notifications** - Alertes de repas
5. **Analytics** - Suivi d'utilisation

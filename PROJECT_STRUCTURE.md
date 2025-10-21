# Structure du Projet JowAfrique

## 📁 Organisation des Dossiers

```
JowAfrique/
├── backend/                    # API Flask
│   ├── api.py                 # API principale (anciennement api_v2.py)
│   ├── database.py            # Gestionnaire de base de données
│   ├── models.py              # Modèles Pydantic
│   ├── security.py            # Sécurité et validation
│   ├── services/              # Services métier
│   │   ├── meal_service.py    # Service des repas
│   │   └── plan_service.py    # Service des plans
│   ├── requirements.txt       # Dépendances Python
│   ├── Dockerfile             # Container Docker
│   └── jowafrique.db          # Base de données SQLite
│
├── frontend/                   # Application Next.js
│   ├── src/
│   │   ├── app/               # Pages Next.js
│   │   ├── components/        # Composants React
│   │   │   ├── ui/            # Composants UI réutilisables
│   │   │   └── *.tsx          # Pages et composants
│   │   ├── hooks/             # Hooks React personnalisés
│   │   ├── lib/               # Utilitaires
│   │   ├── services/          # Services API
│   │   └── types/             # Types TypeScript
│   ├── public/                # Assets statiques
│   ├── package.json           # Dépendances Node.js
│   └── Dockerfile             # Container Docker
│
├── monitoring/                 # Configuration monitoring
│   └── prometheus.yml         # Configuration Prometheus
│
├── scripts/                    # Scripts utilitaires
│   ├── backup.sh              # Sauvegarde base de données
│   └── deploy.sh              # Déploiement
│
├── docker-compose.yml          # Orchestration Docker
├── start.py                    # Démarrage automatique
├── start.ps1                   # Démarrage Windows
├── start_api.py                # Démarrage API uniquement
├── start_api.ps1               # Démarrage API Windows
├── test_api.py                 # Tests API
├── test_integration.py         # Tests d'intégration
└── README.md                   # Documentation principale
```

## 🧹 Nettoyage Effectué

### Fichiers Supprimés
- `backend/app_backup.py` - Ancien backup
- `backend/app_old.py` - Ancienne version
- `backend/app.py` - Ancienne version Streamlit
- `backend/planner_module.py` - Module obsolète
- `backend/pyproject.toml` - Configuration inutile
- `backend/uv.lock` - Lock file inutile
- `backend/setup.ps1` - Script de setup obsolète
- `backend/setup.sh` - Script de setup obsolète
- `backend/README.md` - Documentation dupliquée
- `backend/LICENSE` - Licence dupliquée
- `backend/requirements.txt` - Ancien fichier (renommé requirements_api.txt)
- `backend/venv/` - Environnement virtuel (ne doit pas être versionné)
- `backend/__pycache__/` - Cache Python
- `backend/services/__pycache__/` - Cache Python
- `test_api.py` - Ancien fichier de test (remplacé par test_api_simple.py)

### Hooks Frontend Supprimés
- `frontend/src/hooks/useCache.ts` - Non utilisé
- `frontend/src/hooks/useOfflineSync.ts` - Non utilisé
- `frontend/src/hooks/useRecommendations.ts` - Non utilisé

### Composants Frontend Supprimés
- `frontend/src/components/SearchBar.tsx` - Non utilisé
- `frontend/src/lib/performance.ts` - Non utilisé

### Fichiers Renommés
- `backend/api_v2.py` → `backend/api.py`
- `backend/requirements_api.txt` → `backend/requirements.txt`
- `test_api_simple.py` → `test_api.py`

## 🚀 Scripts de Démarrage

### Démarrage Complet
```bash
python start.py              # Python
.\start.ps1                  # Windows PowerShell
```

### API Uniquement
```bash
python start_api.py          # Python
.\start_api.ps1              # Windows PowerShell
```

### Tests
```bash
python test_api.py           # Tests API
python test_integration.py   # Tests d'intégration
```

## 📦 Dépendances

### Backend (requirements.txt)
- Flask==2.3.3
- Flask-CORS==4.0.0

### Frontend (package.json)
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion
- Axios

## 🔧 Configuration

### Variables d'Environnement
- `FLASK_APP=api.py`
- `FLASK_ENV=production`
- `DB_PATH=jowafrique.db`

### Ports
- Backend API: 5000
- Frontend: 3000
- Prometheus: 9090
- Grafana: 3001

## 📊 Monitoring

- **Prometheus**: Métriques système
- **Grafana**: Tableaux de bord
- **Health Check**: `/api/health`

## 🗄️ Base de Données

- **Type**: SQLite
- **Fichier**: `backend/jowafrique.db`
- **Sauvegarde**: `scripts/backup.sh`

## 🐳 Docker

- **Backend**: `backend/Dockerfile`
- **Frontend**: `frontend/Dockerfile`
- **Orchestration**: `docker-compose.yml`
- **Déploiement**: `scripts/deploy.sh`

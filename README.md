# 🍽️ JowAfrique - Planificateur de Repas Africain

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/your-username/jowafrique)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org)
[![Next.js](https://img.shields.io/badge/next.js-14.0.4-black.svg)](https://nextjs.org)

> Application de planification de repas hebdomadaires spécialement conçue pour l'Afrique, inspirée de Jow mais adaptée aux recettes et ingrédients locaux africains.

## 🌟 Fonctionnalités

- 🍽️ **Planification intelligente** : Génération de plannings hebdomadaires avec IA
- 🇨🇲 **Recettes authentiques** : Base de données de recettes camerounaises et africaines
- 📱 **Interface moderne** : Application Next.js responsive et PWA-ready
- 🔌 **API robuste** : Backend Flask avec base de données SQLite
- ❤️ **Système de favoris** : Sauvegarde des recettes préférées
- ⭐ **Notation** : Système de notation des recettes (1-5 étoiles)
- 📊 **Statistiques** : Suivi des habitudes alimentaires
- 🛒 **Liste de courses** : Génération automatique des ingrédients
- 🎨 **UI/UX moderne** : Interface intuitive avec animations

## 🚀 Démarrage Rapide

### Prérequis
- **Node.js** 18+ et npm
- **Python** 3.8+
- **Git**

### Installation

#### Option 1 : Script automatique (Recommandé)

**Windows (PowerShell)**
```powershell
git clone https://github.com/your-username/jowafrique.git
cd jowafrique
.\start.ps1
```

**Linux/Mac**
```bash
git clone https://github.com/your-username/jowafrique.git
cd jowafrique
python start.py
```

#### Option 2 : Installation manuelle

**Backend**
```bash
cd backend
pip install -r requirements.txt
python api.py
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

### URLs d'accès
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:5000
- **Health Check** : http://localhost:5000/api/health

## 📁 Structure du Projet

```
JowAfrique/
├── 📁 backend/                    # API Flask (Port 5000)
│   ├── 📄 api.py                 # API principale
│   ├── 📄 database.py            # Gestionnaire de base de données
│   ├── 📄 models.py              # Modèles de données
│   ├── 📄 security.py            # Sécurité et validation
│   ├── 📁 services/              # Services métier
│   │   ├── 📄 meal_service.py    # Service des repas
│   │   └── 📄 plan_service.py    # Service des plans
│   ├── 📄 requirements.txt       # Dépendances Python
│   └── 🗄️ jowafrique.db          # Base de données SQLite
│
├── 📁 frontend/                   # Application Next.js (Port 3000)
│   ├── 📁 src/
│   │   ├── 📁 app/               # Pages Next.js 13+
│   │   ├── 📁 components/        # Composants React
│   │   │   ├── 📁 ui/            # Composants UI réutilisables
│   │   │   └── 📄 *.tsx          # Pages et composants
│   │   ├── 📁 hooks/             # Hooks React personnalisés
│   │   ├── 📁 lib/               # Utilitaires
│   │   ├── 📁 services/          # Services API
│   │   └── 📁 types/             # Types TypeScript
│   ├── 📁 public/                # Assets statiques
│   └── 📄 package.json           # Dépendances Node.js
│
├── 📁 monitoring/                 # Configuration monitoring
├── 📁 scripts/                    # Scripts utilitaires
├── 🐳 docker-compose.yml          # Orchestration Docker
├── 📚 Documentation.md            # Documentation complète
├── 📚 API_REFERENCE.md            # Référence API
├── 📚 DEVELOPMENT_GUIDE.md        # Guide de développement
├── 📚 COMPONENTS_GUIDE.md         # Guide des composants
└── 📄 README.md                   # Ce fichier
```

## 🔌 API Documentation

### Endpoints principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/health` | GET | Health check |
| `/api/plans` | GET/POST | Plans hebdomadaires |
| `/api/plans/{id}/meals` | GET/POST | Repas d'un plan |
| `/api/meals/{id}` | PUT | Mettre à jour un repas |
| `/api/meals/{id}/favorite` | POST | Ajouter aux favoris |
| `/api/meals/{id}/rate` | POST | Noter un repas |
| `/api/favorites` | GET | Recettes favorites |
| `/api/statistics` | GET | Statistiques |
| `/api/plans/{id}/shopping-list` | GET | Liste de courses |

### Exemple d'utilisation

```bash
# Récupérer tous les plans
curl http://localhost:5000/api/plans

# Créer un nouveau plan
curl -X POST http://localhost:5000/api/plans \
  -H "Content-Type: application/json" \
  -d '{
    "planName": "Ma Semaine Camerounaise",
    "weekStartDate": "2024-01-15",
    "preferences": {
      "cuisines": ["cameroun"],
      "budget": "modéré"
    }
  }'
```

📖 **Voir [API_REFERENCE.md](API_REFERENCE.md) pour la documentation complète de l'API**

## 🎨 Composants Frontend

### Pages principales
- **MainPage** : Accueil avec repas du jour
- **PlansPage** : Gestion des plans hebdomadaires
- **FavoritesPage** : Recettes favorites
- **StatisticsPage** : Statistiques d'utilisation
- **CartPage** : Liste de courses
- **ProgressPage** : Suivi de préparation
- **SettingsPage** : Paramètres

### Composants UI
- **MealCard** : Carte de repas réutilisable
- **Button** : Bouton avec variantes
- **Card** : Conteneur de contenu
- **LoadingSpinner** : Indicateur de chargement
- **Toast** : Notifications

📖 **Voir [COMPONENTS_GUIDE.md](COMPONENTS_GUIDE.md) pour le guide complet des composants**

## 🗄️ Base de données

### Tables principales

#### `weekly_plans`
```sql
CREATE TABLE weekly_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_name TEXT NOT NULL,
    week_start_date DATE NOT NULL,
    total_budget_estimate REAL,
    generated_by_ai BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### `meal_slots`
```sql
CREATE TABLE meal_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    meal_type TEXT NOT NULL,
    recipe_name TEXT NOT NULL,
    main_ingredient TEXT,
    cuisine_type TEXT,
    prep_time INTEGER,
    cook_time INTEGER,
    is_favorite BOOLEAN DEFAULT 0,
    rating INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (plan_id) REFERENCES weekly_plans(id)
);
```

## 🧪 Tests

### Tests API
```bash
python test_api.py
```

### Tests d'intégration
```bash
python test_integration.py
```

### Tests frontend
```bash
cd frontend
npm test
```

## 🚀 Déploiement

### Docker
```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f
```

### Production
```bash
# Backend avec Gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 api:app

# Frontend
cd frontend
npm run build
npm start
```

## 🔧 Configuration

### Variables d'environnement

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
```

#### Backend
```python
# Dans api.py
DB_PATH = "jowafrique.db"
API_PORT = 5000
```

## 🐛 Dépannage

### Problèmes courants

| Problème | Solution |
|----------|----------|
| CORS Error | Vérifier que Flask-CORS est installé |
| Connection Refused | Vérifier que l'API est démarrée sur le port 5000 |
| Database Error | Vérifier que `jowafrique.db` existe |
| Module not found | Vérifier les imports et les chemins |

### Logs
```bash
# Backend
python api.py

# Frontend
cd frontend && npm run dev
```

## 📚 Documentation

- 📖 **[Documentation Complète](DOCUMENTATION.md)** - Guide complet du projet
- 🔌 **[Référence API](API_REFERENCE.md)** - Documentation détaillée de l'API
- 🛠️ **[Guide de Développement](DEVELOPMENT_GUIDE.md)** - Guide pour les développeurs
- 🎨 **[Guide des Composants](COMPONENTS_GUIDE.md)** - Documentation des composants React

## 🔮 Roadmap

### Fonctionnalités à venir
- [ ] **Authentification** : Système de login utilisateur
- [ ] **IA avancée** : Intégration OpenAI/Claude pour génération de plannings
- [ ] **API Jow** : Intégration avec l'API Jow pour recettes internationales
- [ ] **Real-time** : WebSockets pour notifications
- [ ] **Offline** : Cache local avec Service Worker
- [ ] **Push Notifications** : Alertes de repas
- [ ] **Analytics** : Suivi d'utilisation avancé
- [ ] **Multi-langue** : Support français/anglais
- [ ] **Export** : PDF des plannings et listes de courses

### Améliorations techniques
- [ ] **Tests unitaires** : Couverture complète
- [ ] **CI/CD** : Pipeline de déploiement automatique
- [ ] **Monitoring** : Prometheus + Grafana
- [ ] **Sécurité** : Authentification JWT, rate limiting
- [ ] **Performance** : Cache Redis, optimisations DB

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Équipe

- **Développeur Principal** : [Votre Nom](https://github.com/your-username)
- **Designer UI/UX** : [Nom du Designer](https://github.com/designer-username)
- **Contributeurs** : Voir [CONTRIBUTORS.md](CONTRIBUTORS.md)

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/your-username/jowafrique/issues)
- **Discussions** : [GitHub Discussions](https://github.com/your-username/jowafrique/discussions)
- **Email** : support@jowafrique.com

## 🙏 Remerciements

- [Jow](https://jow.fr) pour l'inspiration
- [Next.js](https://nextjs.org) pour le framework frontend
- [Flask](https://flask.palletsprojects.com/) pour le backend
- [Tailwind CSS](https://tailwindcss.com/) pour le styling
- [Framer Motion](https://www.framer.com/motion/) pour les animations

---

<div align="center">

**Fait avec ❤️ pour l'Afrique**

[🌐 Site Web](https://jowafrique.com) • [📱 App Mobile](https://jowafrique.com/app) • [🐦 Twitter](https://twitter.com/jowafrique) • [📧 Contact](mailto:contact@jowafrique.com)

</div>
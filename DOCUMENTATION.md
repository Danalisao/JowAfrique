# 📚 Documentation Complète - JowAfrique

## 🎯 Vue d'ensemble

**JowAfrique** est une application de planification de dîners hebdomadaires spécialement conçue pour l'Afrique, inspirée de l'application Jow mais adaptée aux recettes et ingrédients locaux africains.

### 🌟 Caractéristiques principales
- **🤖 IA avancée** : Génération de plannings avec Gemini AI 2.5 Flash
- **🍽️ Planification intelligente** : Plannings de dîners hebdomadaires personnalisés
- **🇨🇲 Recettes authentiques** : Base de données de recettes camerounaises et africaines
- **🌍 Intégration Jow** : Recettes internationales via l'API Jow
- **🔄 Système hybride** : Combine recettes locales + Jow avec contraintes intelligentes
- **🚫 Anti-répétition** : Évite les répétitions de repas et ingrédients
- **📱 Interface moderne** : Application Next.js responsive et PWA-ready
- **🔌 API robuste** : Backend Flask avec base de données SQLite
- **❤️ Système de favoris** : Sauvegarde des recettes préférées
- **⭐ Notation** : Système de notation des recettes (1-5 étoiles)
- **📊 Statistiques** : Suivi des habitudes de dîners
- **🛒 Liste de courses** : Génération automatique optimisée par IA
- **🥗 Analyse nutritionnelle** : Équilibre nutritionnel intelligent

---

## 🏗️ Architecture

### 📁 Structure du projet
```
JowAfrique/
├── backend/                    # API Flask (Port 5000)
│   ├── api.py                 # API principale
│   ├── database.py            # Gestionnaire de base de données
│   ├── models.py              # Modèles de données
│   ├── security.py            # Sécurité et validation
│   ├── services/              # Services métier
│   │   ├── meal_service.py    # Service des repas
│   │   └── plan_service.py    # Service des plans
│   ├── requirements.txt       # Dépendances Python
│   └── jowafrique.db          # Base de données SQLite
│
├── frontend/                   # Application Next.js (Port 3000)
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
│   └── package.json           # Dépendances Node.js
│
├── monitoring/                 # Configuration monitoring
├── scripts/                    # Scripts utilitaires
├── docker-compose.yml          # Orchestration Docker
└── Documentation.md            # Cette documentation
```

### 🔄 Flux de données
```
Frontend Next.js (3000) ←→ Backend Flask (5000) ←→ SQLite Database
```

---

## 🚀 Installation et Démarrage

### Prérequis
- **Node.js** 18+ et npm
- **Python** 3.8+
- **Git**
- **Clé API Gemini** : [Obtenir une clé](https://makersuite.google.com/app/apikey)

### Installation rapide

#### Windows (PowerShell)
```powershell
# Cloner le projet
git clone <repository-url>
cd JowAfrique

# Démarrage automatique
.\start.ps1
```

#### Linux/Mac
```bash
# Cloner le projet
git clone <repository-url>
cd JowAfrique

# Démarrage automatique
python start.py
```

### Installation manuelle

#### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python api.py
```

#### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

### URLs d'accès
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:5000
- **Health Check** : http://localhost:5000/api/health

---

## 🔌 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints disponibles

#### 🏥 Health Check
```http
GET /api/health
```
**Réponse :**
```json
{
  "status": "healthy",
  "version": "2.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 📅 Plans hebdomadaires

##### Récupérer tous les plans
```http
GET /api/plans
```
**Réponse :**
```json
[
  {
    "id": 1,
    "plan_name": "Plan Test Cameroun",
    "week_start_date": "2024-01-15",
    "total_budget_estimate": null,
    "generated_by_ai": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

##### Créer un nouveau plan
```http
POST /api/plans
Content-Type: application/json

{
  "planName": "Mon Plan Semaine",
  "weekStartDate": "2024-01-15",
  "preferences": {
    "cuisines": ["cameroun", "asiatique"],
    "budget": "modéré",
    "light": false,
    "vegetarian": false
  },
  "totalBudgetEstimate": 150.0
}
```

##### Récupérer un plan spécifique
```http
GET /api/plans/{plan_id}
```

##### Supprimer un plan
```http
DELETE /api/plans/{plan_id}
```

#### 🍽️ Repas

##### Récupérer les repas d'un plan
```http
GET /api/plans/{plan_id}/meals
```
**Réponse :**
```json
[
  {
    "id": 1,
    "type": "DÉJEUNER",
    "time": "09:00",
    "name": "Poulet DG",
    "calories": "525 kcal",
    "weight": "450 gm",
    "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400",
    "isEditable": true,
    "jowId": null,
    "url": null,
    "ingredient": "Poulet",
    "cuisine": "cameroun",
    "prepTime": 30,
    "cookTime": 45,
    "isFavorite": true,
    "rating": 5,
    "notes": "Recette traditionnelle camerounaise délicieuse"
  }
]
```

##### Ajouter un repas à un plan
```http
POST /api/plans/{plan_id}/meals
Content-Type: application/json

{
  "name": "Ndolé",
  "mealType": "Dîner",
  "ingredient": "Arachides",
  "cuisine": "cameroun",
  "prepTime": 45,
  "cookTime": 60,
  "image": "https://example.com/image.jpg",
  "notes": "Plat national du Cameroun"
}
```

##### Mettre à jour un repas
```http
PUT /api/meals/{meal_id}
Content-Type: application/json

{
  "rating": 5,
  "notes": "Excellent !"
}
```

##### Ajouter aux favoris
```http
POST /api/meals/{meal_id}/favorite
```

##### Noter un repas
```http
POST /api/meals/{meal_id}/rate
Content-Type: application/json

{
  "rating": 4
}
```

#### 📊 Statistiques

##### Statistiques générales
```http
GET /api/statistics
```
**Réponse :**
```json
{
  "totalPlans": 1,
  "totalRecipes": 5,
  "favoriteRecipes": 3,
  "avgRating": 4.2,
  "topIngredients": [
    ["Poulet", 2],
    ["Arachides", 1]
  ]
}
```

##### Statistiques d'un plan
```http
GET /api/plans/{plan_id}/statistics
```

#### 🛒 Liste de courses

##### Générer une liste de courses
```http
GET /api/plans/{plan_id}/shopping-list
```
**Réponse :**
```json
[
  "oignons",
  "tomates",
  "ail",
  "gingembre",
  "huile de palme",
  "piment",
  "cubes maggi",
  "plantain",
  "taro",
  "arachide"
]
```

#### ❤️ Favoris

##### Récupérer les favoris
```http
GET /api/favorites
```

#### 🍳 Repas actuel

##### Repas en cours de préparation
```http
GET /api/current-meal
```

---

## 🎨 Frontend - Composants

### Pages principales

#### 🏠 MainPage
- **Fichier** : `src/components/MainPage.tsx`
- **Fonction** : Page d'accueil avec repas du jour
- **Fonctionnalités** :
  - Affichage des repas planifiés
  - Sélecteur de date
  - Repas en cours de préparation

#### 📅 PlansPage
- **Fichier** : `src/components/PlansPage.tsx`
- **Fonction** : Gestion des plans hebdomadaires
- **Fonctionnalités** :
  - Liste des plans
  - Création de nouveaux plans
  - Sélection de plan actif

#### ❤️ FavoritesPage
- **Fichier** : `src/components/FavoritesPage.tsx`
- **Fonction** : Gestion des recettes favorites
- **Fonctionnalités** :
  - Affichage des favoris
  - Suppression de favoris

#### 📊 StatisticsPage
- **Fichier** : `src/components/StatisticsPage.tsx`
- **Fonction** : Statistiques d'utilisation
- **Fonctionnalités** :
  - Graphiques de consommation
  - Top ingrédients
  - Moyennes de notation

#### 🛒 CartPage
- **Fichier** : `src/components/CartPage.tsx`
- **Fonction** : Liste de courses
- **Fonctionnalités** :
  - Génération automatique
  - Modification manuelle
  - Export/partage

### Composants UI

#### 🍽️ MealCard
- **Fichier** : `src/components/MealCard.tsx`
- **Fonction** : Carte de repas réutilisable
- **Props** :
  - `meal` : Données du repas
  - `onToggleFavorite` : Callback favoris
  - `onRate` : Callback notation
  - `variant` : Style (default, compact, featured)

#### 🎛️ Button
- **Fichier** : `src/components/ui/Button.tsx`
- **Fonction** : Bouton réutilisable
- **Variants** : primary, secondary, outline, ghost, destructive
- **Sizes** : sm, md, lg

#### 🃏 Card
- **Fichier** : `src/components/ui/Card.tsx`
- **Fonction** : Conteneur de contenu
- **Composants** : Card, CardHeader, CardTitle, CardContent

### Hooks personnalisés

#### useMeals
- **Fichier** : `src/hooks/useMeals.ts`
- **Fonction** : Gestion des repas
- **Retour** : `{ meals, loading, error, addMeal, updateMeal, removeMeal, refetch }`

#### useFavorites
- **Fichier** : `src/hooks/useFavorites.ts`
- **Fonction** : Gestion des favoris
- **Retour** : `{ favorites, loading, error, addFavorite, removeFavorite, refetch }`

#### usePlans
- **Fichier** : `src/hooks/usePlans.ts`
- **Fonction** : Gestion des plans
- **Retour** : `{ plans, loading, error, createPlan, deletePlan, refetch }`

---

## 🗄️ Base de données

### Schéma SQLite

#### Table `weekly_plans`
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

#### Table `meal_slots`
```sql
CREATE TABLE meal_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    meal_type TEXT NOT NULL,
    recipe_name TEXT NOT NULL,
    jow_recipe_id TEXT,
    jow_recipe_url TEXT,
    main_ingredient TEXT,
    cuisine_type TEXT,
    image_url TEXT,
    video_url TEXT,
    prep_time INTEGER,
    cook_time INTEGER,
    is_favorite BOOLEAN DEFAULT 0,
    rating INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (plan_id) REFERENCES weekly_plans(id)
);
```

#### Table `favorites`
```sql
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER NOT NULL,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meal_id) REFERENCES meal_slots(id)
);
```

---

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

### Dépendances

#### Backend (requirements.txt)
```
Flask==2.3.3
Flask-CORS==4.0.0
google-generativeai==0.3.2
python-dotenv==1.0.0
requests==2.31.0
```

#### Frontend (package.json)
```json
{
  "dependencies": {
    "next": "14.0.4",
    "react": "^18",
    "react-dom": "^18",
    "tailwindcss": "^3.3.0",
    "framer-motion": "^10.16.16",
    "lucide-react": "^0.294.0",
    "axios": "^1.6.2",
    "clsx": "^2.1.1",
    "tailwind-merge": "^3.3.1"
  }
}
```

---

## 🚀 Déploiement

### Docker

#### Backend
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "api.py"]
```

#### Frontend
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

### Production

#### Backend avec Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

#### Frontend
```bash
npm run build
npm start
```

---

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

---

## 🐛 Debug et Dépannage

### Problèmes courants

#### CORS Error
- **Cause** : Flask-CORS non configuré
- **Solution** : Vérifier l'installation de Flask-CORS

#### Connection Refused
- **Cause** : API non démarrée
- **Solution** : Vérifier que l'API est sur le port 5000

#### Database Error
- **Cause** : Base de données manquante
- **Solution** : Vérifier que `jowafrique.db` existe

### Logs
```bash
# Backend
python api.py

# Frontend
cd frontend && npm run dev
```

---

## 🔄 Système Hybride Jow + Recettes Camerounaises

### Architecture hybride

JowAfrique combine intelligemment deux sources de recettes :

#### 🇨🇲 **Recettes Camerounaises Locales**
- **Base de données locale** : 15+ recettes authentiques camerounaises
- **Recettes populaires** : Ndolé, Poulet DG, Eru, Koki, Achu, etc.
- **Toujours incluses** : Au moins une recette camerounaise par planning
- **Données complètes** : Images, temps de préparation, ingrédients, notes

#### 🌍 **Recettes Jow Internationales**
- **API Jow** : Accès aux recettes internationales
- **Cuisines variées** : Asiatique, mexicaine, française, etc.
- **Enrichissement** : Diversité et variété des plannings
- **Intégration transparente** : Même format que les recettes locales

### Contraintes intelligentes

#### 🚫 **Anti-répétition**
- **Même recette** : Ne revient pas dans les 2 semaines précédentes
- **Ingrédients restreints** : Riz, pâtes max 1 fois par planning
- **Consécutifs interdits** : Riz/pâtes ne se suivent pas sur 2 jours

#### ⚖️ **Équilibre nutritionnel**
- **Diversité** : Minimum 5 ingrédients différents par planning
- **Cuisines variées** : Mix recettes locales + internationales
- **Score qualité** : Évaluation automatique du planning

### Services implémentés

#### `HybridRecipeService`
- Combine recettes Jow + camerounaises
- Applique les contraintes de répétition
- Génère des plannings équilibrés

#### `ConstraintService`
- Gère l'historique des plannings
- Vérifie les violations de contraintes
- Calcule les statistiques de qualité

#### `JowService`
- Interface avec la librairie officielle `jow-api`
- Pas de clé API requise
- Mapping des cuisines
- Formatage des recettes JowResult

### Configuration

```bash
# Variables d'environnement requises
GEMINI_API_KEY=your-gemini-key
# Jow utilise la librairie officielle (pas de clé API requise)

# Installation des dépendances
pip install jow-api

# Initialisation des recettes camerounaises
python backend/scripts/init_cameroon_recipes.py
```

---

## 🤖 Intégration IA - Gemini AI 2.5 Flash

### Configuration
1. **Obtenir une clé API** : [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Configurer l'environnement** :
   ```bash
   # Copier le fichier d'exemple
   cp backend/.env.example backend/.env
   
   # Éditer et ajouter votre clé
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

### Fonctionnalités IA

#### 🍽️ Génération de plannings de dîners
- **Plannings personnalisés** : Basés sur les préférences utilisateur
- **Recettes camerounaises** : Focus sur la cuisine africaine authentique pour le dîner
- **Équilibre nutritionnel** : Analyse automatique des apports des dîners
- **Optimisation budget** : Suggestions selon le budget défini

#### 🔄 Variations de dîners
- **Suggestions créatives** : Variations d'un dîner existant
- **Adaptation culturelle** : Respect des traditions culinaires africaines
- **Substitutions intelligentes** : Alternatives selon les préférences

#### 🛒 Optimisation des courses
- **Liste intelligente** : Génération automatique optimisée
- **Alternatives économiques** : Suggestions d'ingrédients moins chers
- **Saisonnalité** : Recommandations selon les saisons
- **Magasins locaux** : Suggestions de lieux d'achat au Cameroun

#### 📊 Analyse nutritionnelle des dîners
- **Équilibre des macronutriments** : Protéines, glucides, lipides
- **Vitamines et minéraux** : Analyse des apports nutritionnels des dîners
- **Recommandations santé** : Suggestions d'amélioration
- **Score nutritionnel** : Évaluation globale du planning de dîners

### Endpoints IA

#### Générer un planning de dîners
```http
POST /api/ai/generate-plan
Content-Type: application/json

{
  "planName": "Mes Dîners Camerounais",
  "weekStartDate": "2024-01-15",
  "preferences": {
    "cuisines": ["cameroun"],
    "budget": "modéré",
    "light": false,
    "vegetarian": false
  }
}
```

#### Variations de dîners
```http
GET /api/ai/meal-variations/{meal_id}
```

#### Optimiser les courses
```http
POST /api/ai/optimize-shopping/{plan_id}
Content-Type: application/json

{
  "budget": 50.0
}
```

#### Analyse nutritionnelle des dîners
```http
GET /api/ai/nutrition-analysis/{plan_id}
```

#### Régénérer un dîner
```http
POST /api/ai/regenerate-day/{plan_id}
Content-Type: application/json

{
  "day_of_week": "Mardi"
}
```

### Modèles de données IA

#### Réponse de génération de planning de dîners
```json
{
  "success": true,
  "plan_id": 1,
  "meals_added": 7,
  "total_estimated_cost": 56.0,
  "ai_model": "gemini-2.0-flash-exp",
  "statistics": {
    "total_meals": 7,
    "cuisine_distribution": {
      "cameroun": 7
    },
    "top_ingredients": [
      ["Poulet", 3],
      ["Arachides", 2]
    ],
    "avg_prep_time": 32.5,
    "avg_cook_time": 47.2
  },
  "dietary_notes": "Planning de dîners équilibré avec bon apport en protéines"
}
```

#### Analyse nutritionnelle des dîners
```json
{
  "success": true,
  "analysis": {
    "nutritional_score": 8.5,
    "macronutrients": {
      "proteins": "Bon",
      "carbs": "Équilibré",
      "fats": "À améliorer"
    },
    "vitamins_minerals": {
      "vitamin_c": "Excellent",
      "iron": "Bon",
      "calcium": "Moyen"
    },
    "recommendations": [
      "Ajouter plus de légumes verts",
      "Inclure des fruits de saison"
    ],
    "health_benefits": [
      "Riche en protéines",
      "Bonne source de fibres"
    ]
  },
  "ai_model": "gemini-2.0-flash-exp"
}
```

---

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

---

## 📞 Support

### Documentation
- **API** : Voir section API Documentation
- **Frontend** : Voir section Composants
- **Base de données** : Voir section Schéma

### Contact
- **Issues** : Utiliser le système d'issues GitHub
- **Discussions** : Forum de discussion du projet

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

*Documentation générée automatiquement - Dernière mise à jour : 2024-01-15*

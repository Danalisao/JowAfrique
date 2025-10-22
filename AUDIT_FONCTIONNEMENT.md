# 🔍 AUDIT FONCTIONNEMENT - JowAfrique

## Vue d'ensemble rapide

**JowAfrique** = une app de planification de repas africains (spécialisée Cameroun) avec IA (Gemini 2.0 Flash)

**Stack:**
- **Frontend** : Next.js 14 + React 18 + TypeScript + Tailwind CSS
- **Backend** : Flask (Python 3.8+)
- **BD** : SQLite (local)

**Ports:**
- Frontend: 3000
- Backend: 5000

---

## 1️⃣ FLUX GLOBAL DE L'APPLICATION

```
┌─────────────────────────────────────────────────────────────┐
│                    UTILISATEUR                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   FRONTEND (Next.js)   │
         │   http://localhost:3000│
         └────────┬───────────────┘
                  │
    ┌─────────────┴──────────────────┐
    │                                │
    ▼                                ▼
┌──────────────────┐        ┌──────────────────┐
│   useX Hooks     │        │  Composants UI   │
│ (useMeals, etc)  │        │  (MealCard, etc) │
└────────┬─────────┘        └──────────────────┘
         │
         ▼
   ┌──────────┐
   │ api.ts   │ (axios client)
   └────┬─────┘
        │ HTTP JSON
        ▼
    ┌──────────────────────┐
    │ BACKEND (Flask 5000) │
    └────────┬─────────────┘
             │
    ┌────────┴─────────────────────┐
    │                              │
    ▼                              ▼
 ┌─────────────┐           ┌──────────────┐
 │   Services  │           │   Database   │
 │ (meal, plan)│           │    Manager   │
 └─────────────┘           └──────┬───────┘
    │                             │
    │                             ▼
    │                     ┌──────────────────┐
    │                     │  SQLite DB       │
    │                     │ jowafrique.db    │
    │                     └──────────────────┘
    │
    ├─► gemini-ai (via google-generativeai)
    │
    └─► jow-api (recettes internationales)
```

---

## 2️⃣ STRUCTURE BACKEND

### 📁 Fichiers clés

```
backend/
├── api.py ...................... Routeur Flask (17 endpoints)
├── database.py ................. Gestionnaire SQLite
├── models.py ................... Dataclasses (Meal, Plan, UserPreferences)
├── security.py ................. Validation des données
├── services/
│   ├── meal_service.py ......... Logique métier repas
│   ├── plan_service.py ......... Logique métier plans
│   ├── ai_service.py ........... Intégration Gemini AI
│   ├── jow_service.py .......... Intégration API Jow
│   ├── constraint_service.py ... Anti-répétition
│   └── hybrid_recipe_service.py  Combinaison Jow + local
```

### 🗄️ Schéma Base de Données (SQLite)

```sql
weekly_plans
├── id (PK)
├── plan_name
├── week_start_date
├── total_budget_estimate
├── generated_by_ai
└── created_at

meal_slots
├── id (PK)
├── plan_id (FK → weekly_plans)
├── day_of_week ('Lundi', 'Mardi', ...)
├── meal_type ('Petit-déjeuner', 'Déjeuner', 'Dîner')
├── recipe_name
├── jow_recipe_id (optionnel, recettes Jow)
├── main_ingredient
├── cuisine_type ('cameroun', 'asiatique', ...)
├── image_url
├── prep_time
├── cook_time
├── is_favorite (booléen)
├── rating (0-5)
└── notes

favorites
├── id (PK)
├── jow_recipe_id
├── recipe_name
├── cuisine_type
├── image_url
└── added_date

recipe_history
├── id (PK)
├── jow_recipe_id
├── recipe_name
├── used_date
├── plan_id (FK)
└── rating

shopping_lists
├── id (PK)
├── plan_id (FK)
├── ingredients (JSON)
└── created_at
```

### 🔌 Endpoints API (17 au total)

#### Plans
```
GET  /api/plans                    - Récupère tous les plans
POST /api/plans                    - Crée un nouveau plan
GET  /api/plans/{id}               - Récupère 1 plan
DELETE /api/plans/{id}             - Supprime un plan
GET  /api/plans/{id}/statistics    - Stats du plan
```

#### Repas
```
GET  /api/plans/{id}/meals         - Repas d'un plan
POST /api/plans/{id}/meals         - Ajoute repas au plan
PUT  /api/meals/{id}               - Met à jour un repas
DELETE /api/meals/{id}             - Supprime un repas
GET  /api/meals                    - Tous les repas
GET  /api/current-meal             - Repas actuel
POST /api/meals/{id}/favorite      - Ajoute aux favoris
POST /api/meals/{id}/rate          - Note un repas
```

#### Autres
```
GET  /api/statistics               - Stats globales
GET  /api/plans/{id}/shopping-list - Liste de courses
GET  /api/favorites                - Favoris
DELETE /api/favorites/{id}         - Supprime des favoris
GET  /api/health                   - Vérification API
```

#### IA (Gemini 2.0 Flash)
```
POST /api/ai/generate-plan         - Génère un planning avec IA
GET  /api/ai/meal-variations/{id}  - Variations d'un repas
POST /api/ai/optimize-shopping/{id}- Optimise liste courses
GET  /api/ai/nutrition-analysis/{id} - Analyse nutritionnelle
POST /api/ai/regenerate-day/{id}   - Régénère un jour
```

---

## 3️⃣ FLUX D'UTILISATION UTILISATEUR

### Scénario 1: Consulter les repas du jour

```
1. Utilisateur ouvre l'app
   └─→ Frontend charge page.tsx → MainPage

2. MainPage affiche les repas
   └─→ useMeals hook appelé
       └─→ api.getPlanMeals(planId)
           └─→ GET /api/plans/{id}/meals

3. Backend (api.py)
   └─→ plan_service.get_meals_by_plan(plan_id)
       └─→ database.get_plan_meals(plan_id)
           └─→ Query SQLite: SELECT * FROM meal_slots WHERE plan_id = ?
               └─→ Retourne JSON avec repas du jour

4. Frontend reçoit les repas
   └─→ MealCard composants s'affichent
       └─→ Utilisateur voit nom, image, temps, ingrédient, cuisine
```

### Scénario 2: Créer un plan avec IA

```
1. Utilisateur va dans PlansPage → clique "Nouveau plan"

2. Formulaire demande:
   - Nom du plan
   - Date de début de semaine
   - Préférences (cuisines, budget, light, vegetarian)

3. Submit → api.generateAiPlan()
   └─→ POST /api/ai/generate-plan

4. Backend
   └─→ plan_service.generate_ai_plan(preferences)
       ├─→ Crée une WeeklyPlan en BD
       ├─→ Appelle ai_service.generate_weekly_meals()
       │   └─→ Utilise Gemini AI 2.0 Flash
       │       └─→ Génère 7 repas structurés
       │           (jour, type, ingrédient, temps, etc)
       ├─→ constraint_service vérifie pas de répétitions
       ├─→ Ajoute les 7 repas dans meal_slots
       └─→ Retourne les stats du plan créé

5. Frontend affiche confirmation
   └─→ Plan visible dans PlansPage
```

### Scénario 3: Ajouter un repas aux favoris

```
1. Utilisateur clique ❤️ sur un MealCard

2. onToggleFavorite() appelé
   └─→ api.addToFavorites(mealId)
       └─→ POST /api/meals/{id}/favorite

3. Backend
   └─→ meal_service.toggle_favorite(meal_id)
       └─→ database.update_meal(meal_id, {'is_favorite': 1})
           └─→ UPDATE meal_slots SET is_favorite = 1 WHERE id = ?

4. Frontend
   └─→ État local mis à jour
   └─→ Icône ❤️ devient rouge
```

### Scénario 4: Générer une liste de courses

```
1. Utilisateur dans CartPage → clique "Générer"

2. api.generateShoppingList(planId)
   └─→ GET /api/plans/{id}/shopping-list

3. Backend
   └─→ meal_service.generate_shopping_list(plan_id)
       └─→ Récupère tous les repas du plan
           └─→ Extrait les main_ingredient de chaque repas
               └─→ Déduplique (set unique)
                   └─→ Retourne liste: ['oignons', 'tomates', 'ail', ...]

4. Frontend affiche la liste
   └─→ Utilisateur peut cocher items
```

---

## 4️⃣ SERVICES MÉTIER

### MealService (backend/services/meal_service.py)

**Fonctions principales:**
- `get_meals_by_plan(plan_id)` - Repas d'un plan
- `add_meal(meal_data)` - Ajoute un repas
- `update_meal(meal_id, updates)` - Modifie un repas
- `toggle_favorite(meal_id)` - Ajoute/enlève des favoris
- `rate_meal(meal_id, rating)` - Note un repas (1-5)
- `generate_shopping_list(plan_id)` - Liste de courses
- `remove_from_favorites(meal_id)` - Supprime des favoris

### PlanService (backend/services/plan_service.py)

**Fonctions principales:**
- `create_plan(name, date, preferences)` - Crée un plan vide
- `get_plans()` - Tous les plans
- `get_plan_by_id(plan_id)` - 1 plan
- `delete_plan(plan_id)` - Supprime un plan
- `get_plan_statistics(plan_id)` - Stats du plan
- `generate_ai_plan(preferences, name, date)` - **Plan avec IA**

### AIService (backend/services/ai_service.py)

**Intègre Gemini 2.0 Flash API:**
- Génère des repas intelligents avec contraintes
- Analyse nutritionnelle
- Suggestions de variations
- Optimisation budget

### JowService (backend/services/jow_service.py)

**Utilise lib `jow-api` (officielle):**
- Récupère recettes internationales
- Pas besoin de clé API
- Mappe au format interne JowAfrique

### ConstraintService (backend/services/constraint_service.py)

**Applique règles métier:**
- Pas de même recette 2 semaines de suite
- Max 1 riz/pâtes par planning
- Pas 2 jours consécutifs riz + pâtes
- Minimum 5 ingrédients différents

### HybridRecipeService (backend/services/hybrid_recipe_service.py)

**Combine:**
- Recettes locales camerounaises
- Recettes Jow internationales
- Respecte contraintes + préférences

---

## 5️⃣ STRUCTURE FRONTEND

### 📁 Fichiers clés

```
frontend/src/
├── app/
│   └── page.tsx ............... Point d'entrée (SPA)
├── components/
│   ├── MainPage.tsx ........... Page accueil (repas du jour)
│   ├── PlansPage.tsx .......... Gestion plans
│   ├── FavoritesPage.tsx ....... Recettes favorites
│   ├── CartPage.tsx ........... Liste de courses
│   ├── StatisticsPage.tsx ...... Stats
│   ├── ProgressPage.tsx ........ Suivi préparation
│   ├── SettingsPage.tsx ........ Paramètres
│   ├── MealCard.tsx ........... Carte repas (réutilisable)
│   ├── MealVariations.tsx ...... Variations repas
│   ├── NutritionAnalysis.tsx ... Analyse nutritionnelle
│   ├── DesktopNavigation.tsx ... Menu desktop
│   ├── BottomNavigation.tsx .... Menu mobile
│   ├── StatusBar.tsx .......... Barre status
│   └── ui/
│       ├── Button.tsx ......... Bouton réutilisable
│       ├── Card.tsx ........... Conteneur
│       ├── LoadingSpinner.tsx .. Loader
│       ├── StarRating.tsx ...... Étoiles (1-5)
│       └── Toast.tsx .......... Notifications
├── hooks/
│   ├── useMeals.ts ............ État + API repas
│   ├── useFavorites.ts ........ État + API favoris
│   ├── usePlans.ts ............ État + API plans
│   ├── useCurrentMeal.ts ....... Repas actuel
│   ├── useMealActions.ts ....... Actions (note, favori)
│   ├── useSearch.ts ........... Recherche
│   ├── useShoppingList.ts ...... Liste de courses
│   ├── useStatistics.ts ........ Stats
│   └── useAiFeatures.ts ........ Appels IA
├── services/
│   └── api.ts ................. Client axios (tous endpoints)
├── types/
│   └── index.ts ............... Types TypeScript
└── lib/
    └── utils.ts ............... Utilitaires
```

### 🎨 Architecture Composants

```
Home (page.tsx - SPA)
  ├─ MainPage (onglet home)
  │   └─ Affiche repas du jour via useMeals()
  │       └─ MealCard x N
  │           ├─ Image
  │           ├─ Nom, ingrédient
  │           ├─ Temps (prep + cook)
  │           ├─ Étoiles notation
  │           └─ ❤️ favori
  │
  ├─ PlansPage (onglet plans)
  │   └─ Liste des plans + bouton "Créer"
  │       └─ Form création plan
  │           ├─ Préférences (cuisines, budget)
  │           └─ Appel api.generateAiPlan()
  │
  ├─ FavoritesPage (onglet favoris)
  │   └─ MealCard x N (filtrés is_favorite=1)
  │
  ├─ CartPage (onglet courses)
  │   └─ Liste ingrédients
  │       └─ Générée par /api/plans/{id}/shopping-list
  │
  ├─ StatisticsPage (onglet stats)
  │   └─ Graphiques + top ingrédients
  │
  ├─ ProgressPage (onglet préparation)
  │   └─ Suivi de la préparation (pre-cooking, cooking, delivery)
  │
  └─ SettingsPage (onglet paramètres)
      └─ Réglages généraux
```

### 🎣 Hooks React (État centralisé)

Chaque hook gère:
1. État local (`loading`, `error`, `data`)
2. Appels API
3. Refetch/refresh

**Exemple: `useMeals(planId)`**
```typescript
{
  meals: Meal[],
  loading: boolean,
  error: string | null,
  addMeal: (meal: Meal) => Promise<void>,
  updateMeal: (id: number, updates: Partial<Meal>) => Promise<void>,
  removeMeal: (id: number) => Promise<void>,
  refetch: () => Promise<void>
}
```

---

## 6️⃣ FLUX D'UNE REQUÊTE (Exemple: Charger repas)

### 1️⃣ Frontend demande

```typescript
// src/components/MainPage.tsx
const { meals } = useMeals(planId);

// Dans hook useMeals.ts
const [meals, setMeals] = useState<Meal[]>([]);
useEffect(() => {
  const fetchMeals = async () => {
    const response = await api.getPlanMeals(planId);
    if (response.success) setMeals(response.data);
  };
  fetchMeals();
}, [planId]);
```

### 2️⃣ Client API (axios)

```typescript
// src/services/api.ts
export const getPlanMeals = async (planId: number) => {
  try {
    const response = await api.get(`/api/plans/${planId}/meals`);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: '...' };
  }
};
```

### 3️⃣ Requête HTTP

```
GET http://localhost:5000/api/plans/1/meals
Headers: Content-Type: application/json
```

### 4️⃣ Backend reçoit

```python
# backend/api.py
@app.route('/api/plans/<int:plan_id>/meals', methods=['GET'])
def get_plan_meals(plan_id):
    meals_data = meal_service.get_meals_by_plan(plan_id)
    meals = [format_meal_response(meal) for meal in meals_data]
    return jsonify(meals)
```

### 5️⃣ Service métier

```python
# backend/services/meal_service.py
def get_meals_by_plan(self, plan_id: int):
    return self.db_manager.get_plan_meals(plan_id)
```

### 6️⃣ Requête BD

```python
# backend/database.py
def get_plan_meals(self, plan_id: int):
    cursor.execute("""
        SELECT id, day_of_week, meal_type, recipe_name, ...
        FROM meal_slots
        WHERE plan_id = ?
        ORDER BY day_of_week, meal_type
    """, (plan_id,))
    return [dict(row) for row in cursor.fetchall()]
```

### 7️⃣ Format réponse

```json
[
  {
    "id": 1,
    "type": "DÎNER",
    "time": "19:00",
    "name": "Poulet DG",
    "calories": "525 kcal",
    "weight": "450 gm",
    "image": "https://...",
    "ingredient": "Poulet",
    "cuisine": "cameroun",
    "prepTime": 30,
    "cookTime": 45,
    "isFavorite": true,
    "rating": 5,
    "dayOfWeek": "Mardi"
  }
]
```

### 8️⃣ Frontend affiche

```tsx
meals.map(meal => (
  <MealCard 
    key={meal.id}
    meal={meal}
    onToggleFavorite={() => handleFavorite(meal.id)}
    onRate={(rating) => handleRate(meal.id, rating)}
  />
))
```

---

## 7️⃣ ÉTATS DE L'APPLICATION

### Persistent State (BD SQLite)
- Plans hebdomadaires
- Repas + recettes
- Favoris
- Notes/ratings
- Historique

### Local State (Hooks React)
- Tab actif
- Date sélectionnée
- Loading states
- Erreurs

---

## 8️⃣ INTERACTIONS PRINCIPALES

### A. Navigation (SPA)
```
Utilisateur clique sur tab
  → setActiveTab() state change
  → Composant correspondant s'affiche
```

### B. Créer un plan IA
```
Form submit
  → api.generateAiPlan(preferences)
  → Backend: Gemini AI génère 7 repas
  → Stocke dans BD
  → Frontend: Affiche dans PlansPage
```

### C. Ajouter favoris
```
Clic ❤️
  → api.addToFavorites(mealId)
  → Backend: UPDATE is_favorite = 1
  → Frontend: Icône devient rouge
```

### D. Noter un repas
```
Clic étoiles
  → api.rateMeal(mealId, rating)
  → Backend: UPDATE rating = N WHERE id
  → Frontend: Affiche les N étoiles
```

---

## 9️⃣ DÉPENDANCES CRITIQUES

### Backend
```
Flask 2.3.3 ........... Framework web
Flask-CORS 4.0.0 ...... CORS middleware
google-generativeai .... Gemini API
jow-api ............... Recettes internationales
python-dotenv ......... Variables env
requests .............. HTTP client
```

### Frontend
```
Next.js 14 ............ Framework React/SSR
React 18 .............. UI lib
TypeScript ............ Types
Tailwind CSS .......... Styling
Framer Motion ......... Animations
Axios ................. HTTP client
lucide-react .......... Icons
```

---

## 🔟 POINTS CLÉS À RETENIR

### ✅ Ce qui marche bien
1. **Séparation Backend/Frontend** - API REST propre
2. **Services métier** - Logique centralisée en Python
3. **Hooks React** - Gestion état prévisible
4. **BD SQLite** - Simple, portable, performant pour cette app
5. **IA intégrée** - Gemini génère 7 repas rapidement

### ⚠️ Points faibles actuels
1. **Pas d'authentification** - Tous les utilisateurs partagent même BD
2. **Pas de cache** - Chaque requête hit BD
3. **Pas de validation stricte** - Peu de tests
4. **Gestion erreurs légère** - Pas de retry/fallback robustes
5. **CORS simple** - Permet tout (dev only)

### 🚀 Architecture scalable?
- ✅ Structure permet ajout auth facilement
- ✅ Services pourraient être microservices
- ✅ BD pourrait devenir PostgreSQL
- ❌ Pas de cache Redis
- ❌ Pas de file d'attente (IA génération long)

---

## 📊 RÉSUMÉ: Flux utilisateur complet (Jour 1)

```
1. Ouvre l'app (http://localhost:3000)
   └─→ MainPage charge avec repas du jour (plan_id=1)

2. Clique sur "Plans"
   └─→ PlansPage affiche liste des plans

3. Clique "Nouveau plan"
   └─→ Form: nom, date, préférences (cuisine=cameroun, budget=modéré)

4. Submit
   └─→ API génère 7 repas avec Gemini AI
       └─→ Backend: Crée WeeklyPlan + 7 MealSlots
           └─→ BD: INSERT dans weekly_plans + meal_slots

5. Retour MainPage avec nouveau plan
   └─→ Voit repas du jour (lundi dîner)

6. Clique ❤️ sur un repas
   └─→ Passe is_favorite=1 en BD
   └─→ Icône devient rouge

7. Clique sur "Courses"
   └─→ Génère liste ingrédients du plan

8. Clique "Stats"
   └─→ Voit graphiques: top ingrédients, avg rating
```

---

## 📝 Fichiers clés à connaître

| Fichier | Rôle | Ligne |
|---------|------|------|
| `backend/api.py` | Routeur principal | ~517 lignes |
| `backend/database.py` | Accès BD SQLite | ~269 lignes |
| `backend/models.py` | Dataclasses | ~67 lignes |
| `backend/services/meal_service.py` | Logique repas | Variable |
| `backend/services/plan_service.py` | Logique plans | Variable |
| `frontend/src/app/page.tsx` | Root component | 80 lignes |
| `frontend/src/services/api.ts` | Client API | 215 lignes |
| `frontend/src/components/MainPage.tsx` | Repas du jour | Variable |
| `frontend/src/hooks/useMeals.ts` | Hook repas | Variable |

---

*Document généré: Audit complet du fonctionnement de JowAfrique*

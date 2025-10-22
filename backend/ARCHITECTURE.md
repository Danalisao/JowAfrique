# 🏗️ CLEAN ARCHITECTURE - JowAfrique Backend

## Principes

Cette architecture suit les principes de **Clean Architecture** :
- ✅ Séparation des responsabilités (SoC)
- ✅ Une seule source de vérité par concept
- ✅ Pas de dépendances circulaires
- ✅ Facile à tester et maintenir
- ✅ Indépendant des frameworks

---

## 🏛️ Structure en couches

```
┌─────────────────────────────────────────────────────────┐
│                    API LAYER (api.py)                    │
│  HTTP Routes → Input Validation → Service Calls          │
└────────────────────┬────────────────────────────────────┘
                     │ Calls Services
┌────────────────────▼────────────────────────────────────┐
│               SERVICE LAYER (services/)                   │
│  Business Logic → Orchestration → Constraints            │
│                                                           │
│  ├─ MealService (CRUD repas)                            │
│  ├─ PlanService (Plans + IA)                            │
│  ├─ AIService (Intégration Gemini)                      │
│  ├─ JowService (API Jow)                                │
│  ├─ ConstraintService (Anti-répétition)                │
│  └─ HybridRecipeService (Combinaison)                   │
└────────────────────┬────────────────────────────────────┘
                     │ Calls Database
┌────────────────────▼────────────────────────────────────┐
│            DATA ACCESS LAYER (database.py)               │
│  SQL Operations → Transactions → Connection Pool         │
└────────────────────┬────────────────────────────────────┘
                     │ Queries
┌────────────────────▼────────────────────────────────────┐
│               DATABASE (SQLite)                          │
│  Tables: weekly_plans, meal_slots, favorites, etc       │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Structure fichiers

```
backend/
├── api.py                    # ❌ SUPPRIMÉ: planner_module.py
│                             # (logique fusionnée dans services)
├── database.py              # Accès BD (Context Manager)
├── models.py                # Dataclasses (contrats)
├── security.py              # Validation
│
├── services/
│   ├── __init__.py
│   ├── meal_service.py      # Logique repas
│   ├── plan_service.py      # Logique plans + IA (refactorisé)
│   ├── ai_service.py        # Intégration Gemini
│   ├── jow_service.py       # Intégration Jow API
│   ├── constraint_service.py # Contraintes métier
│   └── hybrid_recipe_service.py # Combinaison recettes
│
└── jowafrique.db            # Base de données SQLite
```

---

## 🔄 Flux d'une requête IA (Avant vs Après)

### AVANT (Redondant)
```
api.py
  ↓ import
planner_module.py (IntelligentPlanner)
  ├─ import services/
  └─ Orchestration + Logique (320 lignes)
```
❌ **Problème:** 2 sources de vérité, dépendance circulaire possible

### APRÈS (Clean)
```
api.py (route)
  ↓ appel
plan_service.generate_ai_plan()
  ├─ lazy import MealService
  ├─ lazy import AIService
  ├─ lazy import HybridRecipeService
  └─ Orchestration (orchestration dans service métier)
```
✅ **Avantage:** 
- Une seule source (plan_service)
- Import lazy pour éviter cycles
- Testable directement

---

## 🎯 Responsabilités par couche

### API Layer (api.py)
**Responsabilité:** Routes HTTP, validation input, conversion format

```python
@app.route('/api/plans', methods=['POST'])
def create_plan():
    # 1. Récupérer data JSON
    # 2. Valider champs requis
    # 3. Convertir types (CuisineType, BudgetLevel)
    # 4. Appeler service
    # 5. Retourner JSON
```

**Ne doit PAS faire:**
- ❌ Logique métier complexe
- ❌ Requêtes BD directes
- ❌ Appels API externes

---

### Service Layer (services/)
**Responsabilité:** Logique métier, orchestration, contraintes

#### MealService
```python
- get_meals_by_plan(plan_id)
- add_meal(meal_data)
- toggle_favorite(meal_id)
- rate_meal(meal_id, rating)
- generate_shopping_list(plan_id)
- delete_meal(meal_id)
```

#### PlanService
```python
- create_plan()
- get_plans()
- delete_plan()
- generate_ai_plan() ← ORCHESTRATION
  ├─ Crée plan vide
  ├─ Appelle HybridRecipeService
  ├─ Ajoute repas via MealService
  └─ Retourne stats
```

#### AIService
```python
- generate_content() ← Gemini API
- suggest_meal_variations()
- analyze_nutritional_balance()
- generate_shopping_optimization()
```

#### HybridRecipeService
```python
- generate_weekly_plan_recipes() ← Combine sources
  ├─ 70% recettes locales
  ├─ 30% recettes Jow
  └─ Applique constraints
```

**Ne doit PAS faire:**
- ❌ Formater JSON
- ❌ Gérer sessions HTTP
- ❌ Dépendre de Flask

---

### Data Access Layer (database.py)
**Responsabilité:** SQL, transactions, connection management

```python
class DatabaseManager:
    @contextmanager
    def get_connection(self):
        # Context manager pour transactions
        conn = sqlite3.connect(db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def create_plan(plan: WeeklyPlan) -> int
    def get_plan_meals(plan_id: int) -> List[Dict]
    def update_meal(meal_id: int, updates: Dict) -> bool
    # ... CRUD operations
```

**Ne doit PAS faire:**
- ❌ Logique métier
- ❌ Imports de services
- ❌ Formater réponses

---

### Models (models.py)
**Responsabilité:** Contrats de données, types

```python
@dataclass
class Meal:
    id: Optional[int]
    recipe_name: str
    main_ingredient: Optional[str]
    # ...

@dataclass
class UserPreferences:
    cuisines: List[CuisineType]
    budget: BudgetLevel
    # ...
```

---

## 🧪 Testabilité

### Avant (Difficile à tester)
```python
# test_api.py
def test_generate_plan():
    # Importe planner_module qui importe tous les services
    # Difficile de mocker
    # Dépendances globales
```

### Après (Facile à tester)
```python
# test_plan_service.py
def test_generate_ai_plan():
    db_mock = Mock(DatabaseManager)
    service = PlanService(db_mock)
    
    result = service.generate_ai_plan(prefs, name, date)
    # Facile de tester en isolation
    # Pas de planner_module
```

---

## 🔄 Fluxs d'appels

### 1. Créer un plan vide
```
POST /api/plans
  ↓
api.create_plan()
  ↓
plan_service.create_plan()
  ↓
database.create_plan()
  ↓
INSERT INTO weekly_plans
```

### 2. Générer plan IA
```
POST /api/ai/generate-plan
  ↓
api.generate_ai_plan()
  ↓
plan_service.generate_ai_plan()  ← ORCHESTRATION
  ├─ plan_service.create_plan()
  ├─ hybrid_service.generate_weekly_plan_recipes()
  │  ├─ ai_service.generate_content()  (Gemini)
  │  └─ jow_service.get_recipes()      (API Jow)
  ├─ meal_service.add_meal() x 7
  └─ plan_service.get_plan_statistics()
```

### 3. Ajouter favori
```
POST /api/meals/{id}/favorite
  ↓
api.toggle_favorite()
  ↓
meal_service.toggle_favorite()
  ↓
database.update_meal()
  ↓
UPDATE meal_slots SET is_favorite = 1
```

---

## 🚨 Ce qui a été supprimé

### ❌ planner_module.py (320 lignes)
**Raison:** Redondant avec plan_service

**Logique conservée ✅**
- `generate_weekly_plan()` → `plan_service.generate_ai_plan()`
- `_add_ai_generated_meal()` → `meal_service.add_meal()`
- `_calculate_plan_statistics()` → `plan_service.get_plan_statistics()`

**Import supprimé dans api.py**
```python
# ❌ AVANT
from planner_module import IntelligentPlanner
planner = IntelligentPlanner(db)

# ✅ APRÈS
result = plan_service.generate_ai_plan(...)
```

---

## 📋 Checklist Clean Architecture

- [x] Séparation des responsabilités (API ≠ Service ≠ DB)
- [x] Une seule source de vérité par concept
- [x] Pas de dépendances circulaires
- [x] Import lazy pour éviter cycles
- [x] Services indépendants de Flask
- [x] Database layer avec context manager
- [x] Types stricts (models.py)
- [x] Gestion erreurs cohérente
- [x] Pas de logique globale
- [x] Testable en isolation

---

## 🚀 Améliorations futures

### À court terme
- [ ] Ajouter logger structuré (pas de print())
- [ ] Ajouter validation + exceptions custom
- [ ] Ajouter tests unitaires par service

### À moyen terme
- [ ] Ajouter cache (Redis)
- [ ] Ajouter authentification (JWT)
- [ ] Ajouter monitoring (metrics)

### À long terme
- [ ] Migrer vers ORM (SQLAlchemy)
- [ ] Ajouter event sourcing
- [ ] Déploiement microservices

---

## 📞 Questions?

**Q: Pourquoi lazy imports dans plan_service?**
A: Éviter les imports circulaires. `meal_service` peut avoir besoin de `plan_service`, donc on importe seulement quand on en a besoin.

**Q: Pourquoi pas de planner_module?**
A: Orchestration = responsabilité du service métier, pas d'une classe tierce.

**Q: Comment tester les services?**
A: Mock la DatabaseManager, injecter dans le service, appeler méthode.

---

*Architecture créée: 2024-10-22*
*Version: 1.0 - Clean Architecture*

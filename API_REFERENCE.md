# 🔌 API Reference - JowAfrique

## Base URL
```
http://localhost:5000/api
```

## Authentication
Actuellement, l'API ne nécessite pas d'authentification. Tous les endpoints sont publics.

## Response Format
Toutes les réponses sont au format JSON avec les codes de statut HTTP standard.

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Message d'erreur"
}
```

---

## 📋 Endpoints

### Health Check

#### GET /health
Vérifie l'état de l'API.

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### 📅 Plans hebdomadaires

#### GET /plans
Récupère tous les plans hebdomadaires.

**Response:**
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

#### POST /plans
Crée un nouveau plan hebdomadaire.

**Request Body:**
```json
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

**Response:**
```json
{
  "id": 1,
  "success": true
}
```

#### GET /plans/{plan_id}
Récupère un plan spécifique par son ID.

**Parameters:**
- `plan_id` (int): ID du plan

**Response:**
```json
{
  "id": 1,
  "plan_name": "Plan Test Cameroun",
  "week_start_date": "2024-01-15",
  "total_budget_estimate": null,
  "generated_by_ai": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### DELETE /plans/{plan_id}
Supprime un plan et tous ses repas associés.

**Parameters:**
- `plan_id` (int): ID du plan

**Response:**
```json
{
  "success": true
}
```

#### GET /plans/{plan_id}/statistics
Récupère les statistiques d'un plan spécifique.

**Parameters:**
- `plan_id` (int): ID du plan

**Response:**
```json
{
  "total_meals": 5,
  "avg_rating": 4.2,
  "favorite_count": 3,
  "budget_estimate": 40.0,
  "cuisine_distribution": {
    "cameroun": 5
  }
}
```

---

### 🍽️ Repas

#### GET /plans/{plan_id}/meals
Récupère tous les repas d'un plan.

**Parameters:**
- `plan_id` (int): ID du plan

**Response:**
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

#### POST /plans/{plan_id}/meals
Ajoute un nouveau repas à un plan.

**Parameters:**
- `plan_id` (int): ID du plan

**Request Body:**
```json
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

**Response:**
```json
{
  "id": 2,
  "success": true
}
```

#### PUT /meals/{meal_id}
Met à jour un repas existant.

**Parameters:**
- `meal_id` (int): ID du repas

**Request Body:**
```json
{
  "rating": 5,
  "notes": "Excellent !",
  "isFavorite": true
}
```

**Response:**
```json
{
  "success": true
}
```

#### POST /meals/{meal_id}/favorite
Bascule le statut favori d'un repas.

**Parameters:**
- `meal_id` (int): ID du repas

**Response:**
```json
{
  "success": true
}
```

#### POST /meals/{meal_id}/rate
Note un repas de 1 à 5 étoiles.

**Parameters:**
- `meal_id` (int): ID du repas

**Request Body:**
```json
{
  "rating": 4
}
```

**Response:**
```json
{
  "success": true
}
```

---

### 📊 Statistiques

#### GET /statistics
Récupère les statistiques globales de l'application.

**Response:**
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

---

### 🛒 Liste de courses

#### GET /plans/{plan_id}/shopping-list
Génère une liste de courses pour un plan.

**Parameters:**
- `plan_id` (int): ID du plan

**Response:**
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

---

### ❤️ Favoris

#### GET /favorites
Récupère tous les repas favoris.

**Response:**
```json
[
  {
    "id": 1,
    "type": "DÉJEUNER",
    "name": "Poulet DG",
    "cuisine": "cameroun",
    "rating": 5,
    "added_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 🍳 Repas actuel

#### GET /current-meal
Récupère le repas actuellement en cours de préparation.

**Response:**
```json
{
  "id": 1,
  "type": "DÉJEUNER",
  "name": "Poulet DG",
  "cuisine": "cameroun",
  "prepTime": 30,
  "cookTime": 45,
  "isFavorite": true,
  "rating": 5
}
```

---

## 📝 Types de données

### Plan
```typescript
interface Plan {
  id: number;
  plan_name: string;
  week_start_date: string; // ISO date
  total_budget_estimate?: number;
  generated_by_ai: boolean;
  created_at: string; // ISO datetime
}
```

### Meal
```typescript
interface Meal {
  id: number;
  type: "DÉJEUNER" | "DÎNER";
  time: string; // HH:MM format
  name: string;
  calories: string;
  weight: string;
  image?: string;
  isEditable: boolean;
  jowId?: string;
  url?: string;
  ingredient?: string;
  cuisine: string;
  prepTime?: number;
  cookTime?: number;
  isFavorite: boolean;
  rating: number;
  notes?: string;
}
```

### UserPreferences
```typescript
interface UserPreferences {
  cuisines: string[]; // ["cameroun", "asiatique", "mexican", "french"]
  budget: "économique" | "modéré" | "cher";
  light: boolean;
  vegetarian: boolean;
}
```

### Statistics
```typescript
interface Statistics {
  totalPlans: number;
  totalRecipes: number;
  favoriteRecipes: number;
  avgRating: number;
  topIngredients: [string, number][];
}
```

---

## 🚨 Codes d'erreur

| Code | Description |
|------|-------------|
| 200 | OK - Succès |
| 400 | Bad Request - Données invalides |
| 404 | Not Found - Ressource non trouvée |
| 500 | Internal Server Error - Erreur serveur |

---

## 📚 Exemples d'utilisation

### Créer un plan complet
```bash
# 1. Créer un plan
curl -X POST http://localhost:5000/api/plans \
  -H "Content-Type: application/json" \
  -d '{
    "planName": "Ma Semaine Camerounaise",
    "weekStartDate": "2024-01-15",
    "preferences": {
      "cuisines": ["cameroun"],
      "budget": "modéré",
      "light": false,
      "vegetarian": false
    }
  }'

# 2. Ajouter des repas
curl -X POST http://localhost:5000/api/plans/1/meals \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Poulet DG",
    "mealType": "Déjeuner",
    "ingredient": "Poulet",
    "cuisine": "cameroun",
    "prepTime": 30,
    "cookTime": 45
  }'

# 3. Récupérer le plan avec ses repas
curl http://localhost:5000/api/plans/1/meals
```

### Gérer les favoris
```bash
# Ajouter aux favoris
curl -X POST http://localhost:5000/api/meals/1/favorite

# Noter un repas
curl -X POST http://localhost:5000/api/meals/1/rate \
  -H "Content-Type: application/json" \
  -d '{"rating": 5}'

# Récupérer les favoris
curl http://localhost:5000/api/favorites
```

---

*API Reference - Dernière mise à jour : 2024-01-15*

# 🏗️ CLEAN ARCHITECTURE - Frontend (Next.js)

## Principes

Architecture frontend suivant les mêmes principes que le backend:
- ✅ Séparation des responsabilités (SoC)
- ✅ Pas de logique complexe dans les pages
- ✅ Réutilisabilité des composants
- ✅ Contextes pour état global
- ✅ Hooks pour logique partagée
- ✅ Types stricts (TypeScript)

---

## 🏛️ Structure en couches

```
┌─────────────────────────────────────────────────────────┐
│                    PAGE LAYER (pages/)                   │
│  Routes → Récupère état global → Affiche page           │
└────────────────────┬────────────────────────────────────┘
                     │ Utilise contexte + hooks
┌────────────────────▼────────────────────────────────────┐
│             COMPONENTS LAYER (components/)               │
│                                                           │
│  ├─ Page Components (MainPage, PlansPage, etc)          │
│  │  └─ Utilisent hooks métier + contexte global         │
│  │                                                       │
│  └─ UI Components (Button, Card, etc)                   │
│     └─ Présentationels, pas de logique métier           │
└────────────────────┬────────────────────────────────────┘
                     │ Utilisent hooks
┌────────────────────▼────────────────────────────────────┐
│                HOOKS LAYER (hooks/)                      │
│  Logique métier réutilisable                            │
│                                                           │
│  ├─ useMeals, usePlans, useFavorites (CRUD)            │
│  ├─ useAiFeatures (IA)                                 │
│  └─ useMealActions (Actions combinées)                 │
└────────────────────┬────────────────────────────────────┘
                     │ Appelle api.ts
┌────────────────────▼────────────────────────────────────┐
│              SERVICES LAYER (services/)                  │
│  api.ts: Client HTTP (axios)                            │
│  ├─ Endpoints par domaine métier                        │
│  ├─ Gestion erreurs centralisée                         │
│  └─ Intercepteurs (auth, retry, etc)                    │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Requests
┌────────────────────▼────────────────────────────────────┐
│              BACKEND API (localhost:5000)                │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Structure fichiers

```
frontend/src/
├── app/
│   ├── page.tsx              # Root page (affiche composant actif)
│   ├── layout.tsx            # Layout global (AppProvider wrapper)
│   ├── globals.css
│   └── manifest.json
│
├── components/
│   ├── MainPage.tsx          # Page accueil
│   ├── PlansPage.tsx         # Page plans
│   ├── FavoritesPage.tsx     # Page favoris
│   ├── CartPage.tsx          # Page courses
│   ├── StatisticsPage.tsx    # Page stats
│   ├── ProgressPage.tsx      # Page progression
│   ├── SettingsPage.tsx      # Page paramètres
│   │
│   ├── MealCard.tsx          # Composant réutilisable (carte repas)
│   ├── DatePicker.tsx        # Sélecteur date
│   ├── MealVariations.tsx    # Variations IA
│   ├── NutritionAnalysis.tsx # Analyse nutritionnelle
│   │
│   ├── DesktopNavigation.tsx # Menu desktop
│   ├── BottomNavigation.tsx  # Menu mobile
│   ├── StatusBar.tsx         # Barre status
│   │
│   └── ui/                   # Composants UI purs
│       ├── Button.tsx
│       ├── Card.tsx
│       ├── LoadingSpinner.tsx
│       ├── StarRating.tsx
│       └── Toast.tsx
│
├── providers/
│   └── AppContext.tsx        # Contexte global (état app)
│
├── hooks/
│   ├── useMeals.ts           # État + API repas
│   ├── usePlans.ts           # État + API plans
│   ├── useFavorites.ts       # État + API favoris
│   ├── useShoppingList.ts    # État + API courses
│   ├── useStatistics.ts      # État + API stats
│   ├── useAiFeatures.ts      # État + API IA
│   ├── useMealActions.ts     # Actions (note, fav)
│   ├── useCurrentMeal.ts     # Repas actuel
│   └── useSearch.ts          # Recherche
│
├── services/
│   └── api.ts                # Client HTTP (axios)
│
├── types/
│   └── index.ts              # Interfaces TypeScript
│
└── lib/
    ├── constants.ts          # Constantes (tabs, budgets, etc)
    └── utils.ts              # Utilitaires (formatage, etc)
```

---

## 🎯 Responsabilités par couche

### Page Layer (app/page.tsx)
**Responsabilité:** Afficher la bonne page selon l'onglet actif

```typescript
// ✅ Utilise contexte global
const { activeTab } = useApp()
const CurrentPage = PAGES[activeTab]
return <CurrentPage {...props} />

// ❌ NE DOIT PAS:
// - Gérer useState pour chaque état
// - Afficher tous les if/else
// - Logique métier complexe
```

---

### Component Layer (components/)

#### Page Components
**Responsabilité:** Afficher une page entière

```typescript
export const MainPage = ({ selectedDate, onDateChange, selectedPlanId }) => {
  const { meals, loading } = useMeals(selectedPlanId)
  
  return (
    <div>
      <DatePicker value={selectedDate} onChange={onDateChange} />
      {meals.map(meal => <MealCard key={meal.id} meal={meal} />)}
    </div>
  )
}
```

#### UI Components
**Responsabilité:** Présentation pure (Button, Card, etc)

```typescript
export const Button = ({ children, onClick, variant = 'primary' }) => {
  // ✅ Seulement présentation
  return <button onClick={onClick} className={`btn-${variant}`}>{children}</button>
  
  // ❌ NE DOIT PAS avoir logique métier
}
```

---

### Hooks Layer (hooks/)

**Responsabilité:** Logique métier réutilisable

```typescript
// useMeals.ts
export const useMeals = (planId: number | null) => {
  const [meals, setMeals] = useState<Meal[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (planId) {
      fetchMeals(planId)
    }
  }, [planId])

  return { meals, loading, error, refetch: () => fetchMeals(planId) }
}
```

---

### Services Layer (services/api.ts)

**Responsabilité:** Communication HTTP avec backend

```typescript
// ✅ Organisé par domaine
export const MealsAPI = {
  get: (planId: number) => api.get(`/api/plans/${planId}/meals`),
  add: (planId: number, meal: Meal) => api.post(`/api/plans/${planId}/meals`, meal),
  update: (id: number, updates: Partial<Meal>) => api.put(`/api/meals/${id}`, updates),
  delete: (id: number) => api.delete(`/api/meals/${id}`),
}
```

---

## 🔄 Flux d'une interaction

### Utilisateur clique sur ❤️ Favori

```
1. MealCard component
   └─→ onClick handler
       └─→ Appelle useMealActions().toggleFavorite(meal.id)

2. useMealActions hook
   └─→ Appelle api.MealsAPI.toggleFavorite(meal.id)

3. api.ts
   └─→ POST /api/meals/{id}/favorite

4. Backend
   └─→ UPDATE meal_slots SET is_favorite = 1

5. Frontend reçoit réponse
   └─→ Hook refetch les données
       └─→ Component re-render
           └─→ Icône devient rouge ❤️
```

---

## 🧩 Contexte Global (AppContext)

**Utilisé pour:** États partagés entre pages

```typescript
// app/layout.tsx
<AppProvider>
  <Home />
</AppProvider>

// Dans n'importe quel composant
const { activeTab, setActiveTab, selectedPlanId } = useApp()
```

**Quand l'utiliser:**
- ✅ État partagé entre plusieurs pages
- ✅ Navigation globale
- ✅ Paramètres utilisateur persistants

**Quand NE PAS l'utiliser:**
- ❌ État local d'un composant seul
- ❌ Données temporaires
- ❌ Logique complexe (utiliser hooks à la place)

---

## 📋 Checklist Clean Frontend

- [x] Page.tsx simple (juste affiche composant)
- [x] Contexte global pour état partagé
- [x] Composants: Page vs UI séparés
- [x] Hooks pour logique métier
- [x] API client centralisé (api.ts)
- [x] Types stricts (TypeScript)
- [x] Constants centralisées (constants.ts)
- [x] Pas de logique complexe dans composants
- [x] Props typées
- [x] Gestion erreurs cohérente

---

## 🔄 Patterns utilisés

### Pattern 1: Hook personnalisé pour logique
```typescript
// ✅ Réutilisable
const { meals, loading } = useMeals(planId)

// Dans plusieurs composants
<MainPage /> → useMeals()
<StatisticsPage /> → useMeals()
```

### Pattern 2: Composants présentationnels purs
```typescript
// ✅ Testable, réutilisable
<Button onClick={handleClick}>Click me</Button>
<Card title="Title">Content</Card>
```

### Pattern 3: Contexte pour état global
```typescript
// ✅ Centralise état
const { activeTab, setActiveTab } = useApp()

// Disponible partout
<Navigation activeTab={activeTab} onChange={setActiveTab} />
```

---

## 🚨 Anti-patterns à éviter

### ❌ Logique complexe dans composants
```typescript
// MAUVAIS
const MyPage = () => {
  const [data, setData] = useState(null)
  // 50 lignes de logique complexe
  return <div>...</div>
}

// BON
const MyPage = () => {
  const { data } = useCustomHook()
  return <div>...</div>
}
```

### ❌ Props drilling
```typescript
// MAUVAIS
<Page prop1={x} prop2={y} prop3={z} prop4={w} />
  → <NestedComp prop1={x} prop2={y} />
    → <DeepComp prop1={x} />

// BON
<AppProvider>
  <Page />
    → <NestedComp /> (utilise useApp())
      → <DeepComp /> (utilise useApp())
</AppProvider>
```

### ❌ État dans api.ts
```typescript
// MAUVAIS
export const api = {
  state: { user: null }, // Non!
}

// BON
// État dans hooks/context, pas dans services
```

---

## 🚀 Améliorations futures

### Court terme
- [ ] Ajouter logger (pas console.log)
- [ ] Ajouter error boundaries
- [ ] Ajouter tests unitaires hooks
- [ ] Ajouter tests composants

### Moyen terme
- [ ] Migrate Redux (si état devient trop complexe)
- [ ] Ajouter React Query (cache + sync)
- [ ] Ajouter Zod validation
- [ ] Ajouter E2E tests (Cypress/Playwright)

### Long terme
- [ ] Monorepo (apps/frontend + apps/mobile)
- [ ] Storybook (component library)
- [ ] Design system
- [ ] Analytics tracking

---

## 📞 Questions?

**Q: Pourquoi pas Redux?**
A: Pas besoin pour cet état. Context + hooks suffisant.

**Q: Comment partager logique entre pages?**
A: Créer un hook personnalisé.

**Q: Où mettre la logique de validation?**
A: Dans les hooks ou types/index.ts.

---

*Architecture créée: 2024-10-22*
*Version: 1.0 - Clean Architecture*

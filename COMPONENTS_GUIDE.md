# 🎨 Guide des Composants - JowAfrique

## 📋 Vue d'ensemble

Ce guide détaille tous les composants React de l'application JowAfrique, leurs props, leur utilisation et leurs exemples.

---

## 🏠 Pages principales

### MainPage
**Fichier** : `src/components/MainPage.tsx`

Page d'accueil affichant les repas du jour et le planificateur.

#### Props
```typescript
interface MainPageProps {
  selectedDate: number;           // Jour de la semaine (0-6)
  onDateChange: (date: number) => void;
  selectedPlanId?: number | null; // ID du plan sélectionné
}
```

#### Utilisation
```tsx
<MainPage 
  selectedDate={2} 
  onDateChange={setSelectedDate}
  selectedPlanId={1}
/>
```

#### Fonctionnalités
- Affichage des repas planifiés
- Sélecteur de date
- Repas en cours de préparation
- Gestion des états de chargement et d'erreur

---

### PlansPage
**Fichier** : `src/components/PlansPage.tsx`

Gestion des plans hebdomadaires.

#### Props
```typescript
interface PlansPageProps {
  onSelectPlan: (planId: number) => void;
  selectedPlanId?: number | null;
}
```

#### Utilisation
```tsx
<PlansPage 
  onSelectPlan={setSelectedPlanId}
  selectedPlanId={selectedPlanId}
/>
```

#### Fonctionnalités
- Liste des plans existants
- Création de nouveaux plans
- Sélection de plan actif
- Suppression de plans

---

### FavoritesPage
**Fichier** : `src/components/FavoritesPage.tsx`

Gestion des recettes favorites.

#### Props
Aucune prop requise.

#### Utilisation
```tsx
<FavoritesPage />
```

#### Fonctionnalités
- Affichage des favoris
- Suppression de favoris
- Recherche et filtrage

---

### StatisticsPage
**Fichier** : `src/components/StatisticsPage.tsx`

Statistiques d'utilisation et d'analyse.

#### Props
Aucune prop requise.

#### Utilisation
```tsx
<StatisticsPage />
```

#### Fonctionnalités
- Graphiques de consommation
- Top ingrédients
- Moyennes de notation
- Évolution dans le temps

---

### CartPage
**Fichier** : `src/components/CartPage.tsx`

Liste de courses générée automatiquement.

#### Props
Aucune prop requise.

#### Utilisation
```tsx
<CartPage />
```

#### Fonctionnalités
- Génération automatique
- Modification manuelle
- Export/partage
- Catégorisation des ingrédients

---

### ProgressPage
**Fichier** : `src/components/ProgressPage.tsx`

Suivi de la préparation des repas.

#### Props
```typescript
interface ProgressPageProps {
  stage: 'pre-cooking' | 'cooking' | 'delivery';
  onStageChange: (stage: string) => void;
}
```

#### Utilisation
```tsx
<ProgressPage 
  stage="cooking"
  onStageChange={setProgressStage}
/>
```

#### Fonctionnalités
- Étapes de préparation
- Timer de cuisson
- Notifications
- Suivi du progrès

---

### SettingsPage
**Fichier** : `src/components/SettingsPage.tsx`

Paramètres de l'application.

#### Props
Aucune prop requise.

#### Utilisation
```tsx
<SettingsPage />
```

#### Fonctionnalités
- Préférences utilisateur
- Configuration des notifications
- Gestion du compte
- À propos

---

## 🧩 Composants UI

### MealCard
**Fichier** : `src/components/MealCard.tsx`

Carte de repas réutilisable avec toutes les fonctionnalités.

#### Props
```typescript
interface MealCardProps {
  meal: Meal;                                    // Données du repas
  onEdit?: (meal: Meal) => void;                 // Callback édition
  onToggleFavorite?: (mealId: number) => void;   // Callback favoris
  onRate?: (mealId: number, rating: number) => void; // Callback notation
  planId?: number | null;                        // ID du plan
  variant?: 'default' | 'compact' | 'featured'; // Style de la carte
}
```

#### Utilisation
```tsx
<MealCard 
  meal={mealData}
  onToggleFavorite={handleToggleFavorite}
  onRate={handleRate}
  variant="featured"
/>
```

#### Variants
- **default** : Carte complète avec toutes les informations
- **compact** : Version réduite pour les listes
- **featured** : Mise en avant avec bordure colorée

#### Fonctionnalités
- Affichage des informations du repas
- Boutons d'action (favoris, notation, détails)
- Animations au survol
- Gestion des états de chargement

---

### Button
**Fichier** : `src/components/ui/Button.tsx`

Bouton réutilisable avec plusieurs variantes.

#### Props
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
}
```

#### Utilisation
```tsx
<Button 
  variant="primary" 
  size="md"
  onClick={handleClick}
  loading={isLoading}
>
  Cliquer ici
</Button>

<Button 
  variant="outline" 
  size="sm"
  icon={<Plus size={16} />}
  iconPosition="left"
>
  Ajouter
</Button>
```

#### Variants
- **primary** : Bouton principal (orange)
- **secondary** : Bouton secondaire (gris)
- **outline** : Bouton avec bordure
- **ghost** : Bouton transparent
- **destructive** : Bouton de suppression (rouge)

#### Sizes
- **sm** : Petit (px-3 py-1.5)
- **md** : Moyen (px-4 py-2)
- **lg** : Grand (px-6 py-3)

---

### Card
**Fichier** : `src/components/ui/Card.tsx`

Conteneur de contenu avec header et body.

#### Props
```typescript
interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  clickable?: boolean;
}

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}
```

#### Utilisation
```tsx
<Card hover clickable>
  <CardHeader>
    <CardTitle>Titre de la carte</CardTitle>
  </CardHeader>
  <CardContent>
    Contenu de la carte
  </CardContent>
</Card>
```

#### Fonctionnalités
- Effet de survol optionnel
- Curseur pointer si cliquable
- Styles cohérents
- Composants modulaires

---

### LoadingSpinner
**Fichier** : `src/components/ui/LoadingSpinner.tsx`

Indicateur de chargement animé.

#### Props
```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}
```

#### Utilisation
```tsx
<LoadingSpinner size="md" />
```

---

### Toast
**Fichier** : `src/components/ui/Toast.tsx`

Notification toast pour les messages.

#### Props
```typescript
interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onClose?: () => void;
}
```

#### Utilisation
```tsx
<Toast 
  message="Repas ajouté avec succès !"
  type="success"
  duration={3000}
/>
```

---

## 🧭 Navigation

### BottomNavigation
**Fichier** : `src/components/BottomNavigation.tsx`

Navigation mobile en bas d'écran.

#### Props
```typescript
interface BottomNavigationProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}
```

#### Utilisation
```tsx
<BottomNavigation 
  activeTab="home"
  onTabChange={setActiveTab}
/>
```

#### Onglets
- **home** : Accueil
- **progress** : Progrès
- **favorites** : Favoris
- **settings** : Paramètres
- **cart** : Panier
- **plans** : Plans
- **statistics** : Statistiques

---

### DesktopNavigation
**Fichier** : `src/components/DesktopNavigation.tsx`

Navigation desktop sur le côté.

#### Props
```typescript
interface DesktopNavigationProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}
```

#### Utilisation
```tsx
<DesktopNavigation 
  activeTab="home"
  onTabChange={setActiveTab}
/>
```

---

### StatusBar
**Fichier** : `src/components/StatusBar.tsx`

Barre de statut mobile.

#### Props
Aucune prop requise.

#### Utilisation
```tsx
<StatusBar />
```

---

## 📅 Utilitaires

### DatePicker
**Fichier** : `src/components/DatePicker.tsx`

Sélecteur de date pour la planification.

#### Props
```typescript
interface DatePickerProps {
  selectedDate: number;           // Jour de la semaine (0-6)
  onDateChange: (date: number) => void;
}
```

#### Utilisation
```tsx
<DatePicker 
  selectedDate={2}
  onDateChange={setSelectedDate}
/>
```

#### Fonctionnalités
- Sélection par jour de la semaine
- Affichage des dates
- Navigation entre les semaines

---

## 🎣 Hooks personnalisés

### useMeals
**Fichier** : `src/hooks/useMeals.ts`

Gestion des repas avec API.

#### Retour
```typescript
{
  meals: Meal[];
  loading: boolean;
  error: string | null;
  addMeal: (mealData: Partial<Meal>) => Promise<boolean>;
  updateMeal: (mealId: number, mealData: Partial<Meal>) => Promise<boolean>;
  removeMeal: (mealId: number) => Promise<boolean>;
  refetch: () => Promise<void>;
}
```

#### Utilisation
```tsx
const { meals, loading, error, addMeal, updateMeal } = useMeals(planId);
```

---

### useFavorites
**Fichier** : `src/hooks/useFavorites.ts`

Gestion des favoris.

#### Retour
```typescript
{
  favorites: Meal[];
  loading: boolean;
  error: string | null;
  addFavorite: (mealId: number) => Promise<boolean>;
  removeFavorite: (mealId: number) => Promise<boolean>;
  refetch: () => Promise<void>;
}
```

#### Utilisation
```tsx
const { favorites, addFavorite, removeFavorite } = useFavorites();
```

---

### usePlans
**Fichier** : `src/hooks/usePlans.ts`

Gestion des plans.

#### Retour
```typescript
{
  plans: Plan[];
  loading: boolean;
  error: string | null;
  createPlan: (planData: PlanData) => Promise<boolean>;
  deletePlan: (planId: number) => Promise<boolean>;
  refetch: () => Promise<void>;
}
```

#### Utilisation
```tsx
const { plans, createPlan, deletePlan } = usePlans();
```

---

## 🎨 Styles et thème

### Classes CSS personnalisées
```css
/* Boutons */
.btn-primary { /* Bouton principal */ }
.btn-secondary { /* Bouton secondaire */ }
.btn-outline { /* Bouton avec bordure */ }

/* Cartes */
.meal-card-grid { /* Grille des cartes de repas */ }
.hero-container { /* Container hero */ }
.hero-title { /* Titre principal */ }
.hero-subtitle { /* Sous-titre */ }

/* Layout */
.desktop-main { /* Layout desktop */ }
```

### Variables CSS
```css
:root {
  --light-cream: #fefcf3;
  --primary-500: #f97316;
  --brown-600: #92400e;
  --brown-900: #451a03;
}
```

---

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile first */
sm: 640px    /* Small devices */
md: 768px    /* Medium devices */
lg: 1024px   /* Large devices */
xl: 1280px   /* Extra large devices */
2xl: 1536px  /* 2X large devices */
```

### Classes responsive
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* Grille responsive */}
</div>

<div className="px-2 sm:px-4 md:px-6 lg:px-8">
  {/* Padding responsive */}
</div>
```

---

## 🧪 Tests des composants

### Exemple de test
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import MealCard from '@/components/MealCard';

describe('MealCard', () => {
  const mockMeal = {
    id: 1,
    name: 'Poulet DG',
    cuisine: 'cameroun',
    rating: 5,
    isFavorite: true
  };

  it('affiche le nom du repas', () => {
    render(<MealCard meal={mockMeal} />);
    expect(screen.getByText('Poulet DG')).toBeInTheDocument();
  });

  it('appelle onToggleFavorite au clic', () => {
    const mockToggle = jest.fn();
    render(<MealCard meal={mockMeal} onToggleFavorite={mockToggle} />);
    
    fireEvent.click(screen.getByRole('button', { name: /favorite/i }));
    expect(mockToggle).toHaveBeenCalledWith(1);
  });
});
```

---

*Guide des composants - Dernière mise à jour : 2024-01-15*

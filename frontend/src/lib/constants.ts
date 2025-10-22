/**
 * Constantes de l'application Frontend
 * Centralisées pour éviter la duplication
 */

// Types de tabs (navigation)
export const NAVIGATION_TABS = {
  HOME: 'home',
  PROGRESS: 'progress',
  FAVORITES: 'favorites',
  SETTINGS: 'settings',
  CART: 'cart',
  PLANS: 'plans',
  STATISTICS: 'statistics',
} as const

export type NavigationTab = typeof NAVIGATION_TABS[keyof typeof NAVIGATION_TABS]

// Labels pour UI
export const TAB_LABELS: Record<NavigationTab, string> = {
  [NAVIGATION_TABS.HOME]: 'Accueil',
  [NAVIGATION_TABS.PROGRESS]: 'Préparation',
  [NAVIGATION_TABS.FAVORITES]: 'Favoris',
  [NAVIGATION_TABS.SETTINGS]: 'Paramètres',
  [NAVIGATION_TABS.CART]: 'Courses',
  [NAVIGATION_TABS.PLANS]: 'Plans',
  [NAVIGATION_TABS.STATISTICS]: 'Statistiques',
}

// Émojis pour navigation
export const TAB_EMOJIS: Record<NavigationTab, string> = {
  [NAVIGATION_TABS.HOME]: '🏠',
  [NAVIGATION_TABS.PROGRESS]: '⏳',
  [NAVIGATION_TABS.FAVORITES]: '❤️',
  [NAVIGATION_TABS.SETTINGS]: '⚙️',
  [NAVIGATION_TABS.CART]: '🛒',
  [NAVIGATION_TABS.PLANS]: '📅',
  [NAVIGATION_TABS.STATISTICS]: '📊',
}

// États de progression
export const PROGRESS_STAGES = {
  PRE_COOKING: 'pre-cooking',
  COOKING: 'cooking',
  DELIVERY: 'delivery',
} as const

export type ProgressStage = typeof PROGRESS_STAGES[keyof typeof PROGRESS_STAGES]

// Types de repas
export const MEAL_TYPES = {
  BREAKFAST: 'Petit-déjeuner',
  LUNCH: 'Déjeuner',
  DINNER: 'Dîner',
} as const

// Budget levels
export const BUDGET_LEVELS = {
  ECONOMIC: 'économique',
  MODERATE: 'modéré',
  EXPENSIVE: 'cher',
} as const

// Jours de la semaine
export const DAYS_OF_WEEK = [
  'Lundi',
  'Mardi',
  'Mercredi',
  'Jeudi',
  'Vendredi',
  'Samedi',
  'Dimanche',
] as const

// Cuisines disponibles
export const CUISINES = {
  CAMEROON: 'cameroun',
  ASIAN: 'asiatique',
  MEXICAN: 'mexican',
  FRENCH: 'french',
} as const

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  TIMEOUT: 30000, // ms
  RETRY_ATTEMPTS: 3,
} as const

// UI Configuration
export const UI_CONFIG = {
  TOAST_DURATION: 3000, // ms
  ANIMATION_DURATION: 300, // ms
  DEBOUNCE_DELAY: 300, // ms
} as const

// Valeurs par défaut
export const DEFAULT_VALUES = {
  SELECTED_PLAN_ID: 1,
  SELECTED_DATE: 2, // Mardi
  PAGE_SIZE: 20,
} as const

// Messages d'erreur
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Serveur non disponible. Vérifiez que le backend est démarré.',
  GENERIC_ERROR: 'Une erreur est survenue. Veuillez réessayer.',
  PLAN_CREATION_ERROR: 'Erreur lors de la création du plan',
  MEAL_UPDATE_ERROR: 'Erreur lors de la mise à jour du repas',
  FETCH_ERROR: 'Erreur lors de la récupération des données',
} as const

// Messages de succès
export const SUCCESS_MESSAGES = {
  PLAN_CREATED: 'Plan créé avec succès!',
  PLAN_DELETED: 'Plan supprimé avec succès!',
  MEAL_ADDED: 'Repas ajouté avec succès!',
  FAVORITE_ADDED: 'Ajouté aux favoris!',
  FAVORITE_REMOVED: 'Retiré des favoris!',
  MEAL_RATED: 'Note mise à jour!',
} as const

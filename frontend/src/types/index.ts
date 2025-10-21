export interface Meal {
  id: number
  type: 'DÉJEUNER' | 'DÎNER'
  time?: string
  name: string
  calories: string
  weight?: string
  image: string | null
  isEditable: boolean
  jowId?: string
  url?: string
  videoUrl?: string
  ingredient?: string
  cuisine?: string
  prepTime?: number
  cookTime?: number
  isFavorite?: boolean
  rating?: number
  notes?: string
  dayOfWeek?: string
  mealType?: string
}

export interface WeeklyPlan {
  id: number
  planName: string
  weekStartDate: string
  totalBudgetEstimate?: number
  generatedByAi: boolean
  createdAt: string
}

export interface ProgressStage {
  stage: 'pre-cooking' | 'cooking' | 'delivery'
  timeLeft: {
    hours: number
    minutes: number
    seconds: number
  }
  progress: number
  message: string
}

export interface UserPreferences {
  cuisines: string[]
  budget: 'économique' | 'modéré' | 'cher'
  light: boolean
  vegetarian: boolean
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

export interface Statistics {
  totalPlans: number
  totalRecipes: number
  favoriteRecipes: number
  avgRating: number
  topIngredients: Array<[string, number]>
}

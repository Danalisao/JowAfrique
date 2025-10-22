import axios from 'axios'
import { WeeklyPlan, Meal, UserPreferences, Statistics, ApiResponse } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // Augmenté pour les requêtes IA
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour gérer les erreurs globalement
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNREFUSED') {
      console.error('API non disponible. Vérifiez que le backend est démarré sur le port 5000.')
    }
    return Promise.reject(error)
  }
)

// Weekly Plans
export const getWeeklyPlans = async (): Promise<ApiResponse<WeeklyPlan[]>> => {
  try {
    const response = await api.get('/api/plans')
    return { success: true, data: response.data }
  } catch (error: any) {
    console.error('Erreur API getWeeklyPlans:', error)
    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      return { success: false, error: 'Serveur non disponible. Vérifiez que le backend est démarré.' }
    }
    return { success: false, error: error.response?.data?.message || 'Erreur lors de la récupération des plans' }
  }
}

export const createWeeklyPlan = async (planData: {
  planName: string
  weekStartDate: string
  preferences: UserPreferences
}): Promise<ApiResponse<WeeklyPlan>> => {
  try {
    const response = await api.post('/api/plans', planData)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la création du plan' }
  }
}

export const deleteWeeklyPlan = async (planId: number): Promise<ApiResponse<void>> => {
  try {
    await api.delete(`/api/plans/${planId}`)
    return { success: true }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la suppression du plan' }
  }
}

// Meals
export const getMeals = async (): Promise<ApiResponse<Meal[]>> => {
  try {
    const response = await api.get('/api/meals')
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la récupération des repas' }
  }
}

export const getCurrentMeal = async (): Promise<ApiResponse<Meal>> => {
  try {
    const response = await api.get('/api/current-meal')
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la récupération du repas actuel' }
  }
}

export const getPlanMeals = async (planId: number): Promise<ApiResponse<Meal[]>> => {
  try {
    const response = await api.get(`/api/plans/${planId}/meals`)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la récupération des repas' }
  }
}

export const addMealToPlan = async (planId: number, mealData: Partial<Meal>): Promise<ApiResponse<Meal>> => {
  try {
    const response = await api.post(`/api/plans/${planId}/meals`, mealData)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de l\'ajout du repas' }
  }
}

export const updateMeal = async (mealId: number, mealData: Partial<Meal>): Promise<ApiResponse<Meal>> => {
  try {
    const response = await api.put(`/api/meals/${mealId}`, mealData)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la mise à jour du repas' }
  }
}

export const deleteMeal = async (mealId: number): Promise<ApiResponse<void>> => {
  try {
    await api.delete(`/api/meals/${mealId}`)
    return { success: true }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la suppression du repas' }
  }
}

// Favorites
export const getFavorites = async (): Promise<ApiResponse<Meal[]>> => {
  try {
    const response = await api.get('/api/favorites')
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la récupération des favoris' }
  }
}

export const addToFavorites = async (mealId: number): Promise<ApiResponse<void>> => {
  try {
    await api.post(`/api/meals/${mealId}/favorite`)
    return { success: true }
  } catch (error) {
    return { success: false, error: 'Erreur lors de l\'ajout aux favoris' }
  }
}

export const removeFromFavorites = async (mealId: number): Promise<ApiResponse<void>> => {
  try {
    await api.delete(`/api/favorites/${mealId}`)
    return { success: true }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la suppression des favoris' }
  }
}

// Statistics
export const getStatistics = async (): Promise<ApiResponse<Statistics>> => {
  try {
    const response = await api.get('/api/statistics')
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la récupération des statistiques' }
  }
}

// Shopping List
export const generateShoppingList = async (planId: number): Promise<ApiResponse<string[]>> => {
  try {
    const response = await api.get(`/api/plans/${planId}/shopping-list`)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la génération de la liste de courses' }
  }
}

// AI Endpoints
export const generateAiPlan = async (planData: {
  planName: string
  weekStartDate: string
  preferences: UserPreferences
}): Promise<ApiResponse<WeeklyPlan>> => {
  try {
    const response = await api.post('/api/ai/generate-plan', planData)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la génération du plan IA' }
  }
}

export const getMealVariations = async (mealId: number): Promise<ApiResponse<any[]>> => {
  try {
    const response = await api.get(`/api/ai/meal-variations/${mealId}`)
    return { success: true, data: response.data.variations }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la récupération des variations' }
  }
}

export const optimizeShoppingList = async (planId: number, budget?: number): Promise<ApiResponse<any>> => {
  try {
    const response = await api.post(`/api/ai/optimize-shopping/${planId}`, { budget })
    return { success: true, data: response.data.optimization }
  } catch (error) {
    return { success: false, error: 'Erreur lors de l\'optimisation de la liste' }
  }
}

export const analyzeNutrition = async (planId: number): Promise<ApiResponse<any>> => {
  try {
    const response = await api.get(`/api/ai/nutrition-analysis/${planId}`)
    return { success: true, data: response.data.analysis }
  } catch (error) {
    return { success: false, error: 'Erreur lors de l\'analyse nutritionnelle' }
  }
}

export const regeneratePlanDay = async (planId: number, dayOfWeek: string): Promise<ApiResponse<any>> => {
  try {
    const response = await api.post(`/api/ai/regenerate-day/${planId}`, { day_of_week: dayOfWeek })
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: 'Erreur lors de la régénération du jour' }
  }
}

export default api

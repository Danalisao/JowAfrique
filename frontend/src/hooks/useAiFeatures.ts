'use client'

import { useState } from 'react'
import { 
  generateAiPlan, 
  getMealVariations, 
  optimizeShoppingList, 
  analyzeNutrition, 
  regeneratePlanDay 
} from '@/services/api'
import { UserPreferences } from '@/types'

export const useAiFeatures = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const generatePlanWithAi = async (planData: {
    planName: string
    weekStartDate: string
    preferences: UserPreferences
  }) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await generateAiPlan(planData)
      if (response.success) {
        return response.data
      } else {
        setError(response.error || 'Erreur lors de la génération du plan IA')
        return null
      }
    } catch (err) {
      setError('Erreur de connexion à l\'IA')
      return null
    } finally {
      setLoading(false)
    }
  }

  const getVariations = async (mealId: number) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await getMealVariations(mealId)
      if (response.success) {
        return response.data
      } else {
        setError(response.error || 'Erreur lors de la récupération des variations')
        return null
      }
    } catch (err) {
      setError('Erreur de connexion à l\'IA')
      return null
    } finally {
      setLoading(false)
    }
  }

  const optimizeShopping = async (planId: number, budget?: number) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await optimizeShoppingList(planId, budget)
      if (response.success) {
        return response.data
      } else {
        setError(response.error || 'Erreur lors de l\'optimisation')
        return null
      }
    } catch (err) {
      setError('Erreur de connexion à l\'IA')
      return null
    } finally {
      setLoading(false)
    }
  }

  const analyzePlanNutrition = async (planId: number) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await analyzeNutrition(planId)
      if (response.success) {
        return response.data
      } else {
        setError(response.error || 'Erreur lors de l\'analyse nutritionnelle')
        return null
      }
    } catch (err) {
      setError('Erreur de connexion à l\'IA')
      return null
    } finally {
      setLoading(false)
    }
  }

  const regenerateDay = async (planId: number, dayOfWeek: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await regeneratePlanDay(planId, dayOfWeek)
      if (response.success) {
        return response.data
      } else {
        setError(response.error || 'Erreur lors de la régénération')
        return null
      }
    } catch (err) {
      setError('Erreur de connexion à l\'IA')
      return null
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    generatePlanWithAi,
    getVariations,
    optimizeShopping,
    analyzePlanNutrition,
    regenerateDay,
    clearError: () => setError(null)
  }
}

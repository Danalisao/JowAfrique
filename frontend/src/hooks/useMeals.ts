'use client'

import { useState, useEffect } from 'react'
import { Meal } from '@/types'
import { getPlanMeals, addMealToPlan, updateMeal, deleteMeal, getMeals } from '@/services/api'

export const useMeals = (planId: number | null) => {
  const [meals, setMeals] = useState<Meal[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchMeals = async () => {
    if (!planId) return
    
    setLoading(true)
    setError(null)
    
    const response = await getPlanMeals(planId)
    
    if (response.success && response.data) {
      setMeals(response.data)
    } else {
      setError(response.error || 'Erreur lors du chargement des repas')
    }
    
    setLoading(false)
  }

  const addMeal = async (mealData: Partial<Meal>) => {
    if (!planId) return false
    
    const response = await addMealToPlan(planId, mealData)
    
    if (response.success) {
      await fetchMeals() // Refresh the list
      return true
    } else {
      setError(response.error || 'Erreur lors de l\'ajout du repas')
      return false
    }
  }

  const updateMealById = async (mealId: number, mealData: Partial<Meal>) => {
    const response = await updateMeal(mealId, mealData)
    
    if (response.success) {
      setMeals(prev => prev.map(meal => 
        meal.id === mealId ? { ...meal, ...mealData } : meal
      ))
      return true
    } else {
      setError(response.error || 'Erreur lors de la mise à jour du repas')
      return false
    }
  }

  const removeMeal = async (mealId: number) => {
    const response = await deleteMeal(mealId)
    
    if (response.success) {
      setMeals(prev => prev.filter(meal => meal.id !== mealId))
      return true
    } else {
      setError(response.error || 'Erreur lors de la suppression du repas')
      return false
    }
  }

  useEffect(() => {
    fetchMeals()
  }, [planId])

  return {
    meals,
    loading,
    error,
    addMeal,
    updateMeal: updateMealById,
    removeMeal,
    refetch: fetchMeals
  }
}

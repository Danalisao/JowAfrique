'use client'

import { useState } from 'react'
import { updateMeal } from '@/services/api'

export const useMealActions = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const rateMeal = async (mealId: number, rating: number) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await updateMeal(mealId, { rating })
      if (response.success) {
        return true
      } else {
        setError(response.error || 'Erreur lors de la notation')
        return false
      }
    } catch (err) {
      setError('Erreur de connexion')
      return false
    } finally {
      setLoading(false)
    }
  }

  const toggleFavorite = async (mealId: number) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await updateMeal(mealId, { isFavorite: true })
      if (response.success) {
        return true
      } else {
        setError(response.error || 'Erreur lors de l\'ajout aux favoris')
        return false
      }
    } catch (err) {
      setError('Erreur de connexion')
      return false
    } finally {
      setLoading(false)
    }
  }

  const addNotes = async (mealId: number, notes: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await updateMeal(mealId, { notes })
      if (response.success) {
        return true
      } else {
        setError(response.error || 'Erreur lors de l\'ajout des notes')
        return false
      }
    } catch (err) {
      setError('Erreur de connexion')
      return false
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    rateMeal,
    toggleFavorite,
    addNotes,
    clearError: () => setError(null)
  }
}

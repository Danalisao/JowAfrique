'use client'

import { useState, useEffect } from 'react'
import { Meal } from '@/types'
import { getFavorites, addToFavorites, removeFromFavorites } from '@/services/api'

export const useFavorites = () => {
  const [favorites, setFavorites] = useState<Meal[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchFavorites = async () => {
    setLoading(true)
    setError(null)
    
    const response = await getFavorites()
    
    if (response.success && response.data) {
      setFavorites(response.data)
    } else {
      setError(response.error || 'Erreur lors du chargement des favoris')
    }
    
    setLoading(false)
  }

  const addFavorite = async (mealId: number) => {
    const response = await addToFavorites(mealId)
    
    if (response.success) {
      await fetchFavorites() // Refresh the list
      return true
    } else {
      setError(response.error || 'Erreur lors de l\'ajout aux favoris')
      return false
    }
  }

  const removeFavorite = async (mealId: number) => {
    const response = await removeFromFavorites(mealId)
    
    if (response.success) {
      setFavorites(prev => prev.filter(fav => fav.id !== mealId))
      return true
    } else {
      setError(response.error || 'Erreur lors de la suppression des favoris')
      return false
    }
  }

  useEffect(() => {
    fetchFavorites()
  }, [])

  return {
    favorites,
    loading,
    error,
    addFavorite,
    removeFavorite,
    refetch: fetchFavorites
  }
}

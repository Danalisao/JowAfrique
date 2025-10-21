'use client'

import { useState, useEffect } from 'react'
import { Meal } from '@/types'
import { getCurrentMeal } from '@/services/api'

export const useCurrentMeal = () => {
  const [currentMeal, setCurrentMeal] = useState<Meal | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchCurrentMeal = async () => {
    setLoading(true)
    setError(null)
    
    const response = await getCurrentMeal()
    
    if (response.success && response.data) {
      setCurrentMeal(response.data)
    } else {
      setError(response.error || 'Erreur lors du chargement du repas actuel')
    }
    
    setLoading(false)
  }

  useEffect(() => {
    fetchCurrentMeal()
  }, [])

  return {
    currentMeal,
    loading,
    error,
    refetch: fetchCurrentMeal
  }
}

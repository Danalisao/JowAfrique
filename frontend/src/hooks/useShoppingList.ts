'use client'

import { useState } from 'react'
import { generateShoppingList } from '@/services/api'

export const useShoppingList = () => {
  const [ingredients, setIngredients] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const generateList = async (planId: number) => {
    setLoading(true)
    setError(null)
    
    const response = await generateShoppingList(planId)
    
    if (response.success && response.data) {
      setIngredients(response.data)
    } else {
      setError(response.error || 'Erreur lors de la génération de la liste')
    }
    
    setLoading(false)
  }

  const clearList = () => {
    setIngredients([])
    setError(null)
  }

  return {
    ingredients,
    loading,
    error,
    generateList,
    clearList
  }
}

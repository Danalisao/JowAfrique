'use client'

import { useState, useEffect } from 'react'
import { WeeklyPlan, UserPreferences } from '@/types'
import { getWeeklyPlans, createWeeklyPlan, deleteWeeklyPlan } from '@/services/api'

export const usePlans = () => {
  const [plans, setPlans] = useState<WeeklyPlan[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchPlans = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await getWeeklyPlans()
      
      if (response.success && response.data) {
        setPlans(response.data)
      } else {
        setError(response.error || 'Erreur lors du chargement des plans')
      }
    } catch (error) {
      console.error('Erreur lors du chargement des plans:', error)
      setError('Impossible de se connecter au serveur. Vérifiez que le backend est démarré.')
    } finally {
      setLoading(false)
    }
  }

  const createPlan = async (planData: {
    planName: string
    weekStartDate: string
    preferences: UserPreferences
  }) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await createWeeklyPlan(planData)
      
      if (response.success && response.data) {
        setPlans(prev => [response.data!, ...prev])
        return response.data
      } else {
        setError(response.error || 'Erreur lors de la création du plan')
        return null
      }
    } finally {
      setLoading(false)
    }
  }

  const removePlan = async (planId: number) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await deleteWeeklyPlan(planId)
      
      if (response.success) {
        setPlans(prev => prev.filter(plan => plan.id !== planId))
        return true
      } else {
        setError(response.error || 'Erreur lors de la suppression du plan')
        return false
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPlans()
  }, [])

  return {
    plans,
    loading,
    error,
    createPlan,
    removePlan,
    refetch: fetchPlans
  }
}

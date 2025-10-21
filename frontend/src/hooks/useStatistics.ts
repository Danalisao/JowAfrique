'use client'

import { useState, useEffect } from 'react'
import { Statistics } from '@/types'
import { getStatistics } from '@/services/api'

export const useStatistics = () => {
  const [statistics, setStatistics] = useState<Statistics | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchStatistics = async () => {
    setLoading(true)
    setError(null)
    
    const response = await getStatistics()
    
    if (response.success && response.data) {
      setStatistics(response.data)
    } else {
      setError(response.error || 'Erreur lors du chargement des statistiques')
    }
    
    setLoading(false)
  }

  useEffect(() => {
    fetchStatistics()
  }, [])

  return {
    statistics,
    loading,
    error,
    refetch: fetchStatistics
  }
}

'use client'

import { useState, useEffect } from 'react'
import { Clock, ChefHat, Rocket } from 'lucide-react'
import MealCard from './MealCard'
import { Meal } from '@/types'

interface ProgressPageProps {
  stage: 'pre-cooking' | 'cooking' | 'delivery'
  onStageChange: (stage: 'pre-cooking' | 'cooking' | 'delivery') => void
}

export default function ProgressPage({ stage, onStageChange }: ProgressPageProps) {
  const [timeLeft, setTimeLeft] = useState({
    hours: 1,
    minutes: 20,
    seconds: 37
  })

  const [progress, setProgress] = useState(0)

  // Timer effect
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        let { hours, minutes, seconds } = prev
        
        if (seconds > 0) {
          seconds--
        } else if (minutes > 0) {
          minutes--
          seconds = 59
        } else if (hours > 0) {
          hours--
          minutes = 59
          seconds = 59
        } else {
          // Timer finished, move to next stage
          if (stage === 'pre-cooking') {
            onStageChange('cooking')
            return { hours: 0, minutes: 20, seconds: 21 }
          } else if (stage === 'cooking') {
            onStageChange('delivery')
            return { hours: 0, minutes: 8, seconds: 12 }
          }
        }
        
        return { hours, minutes, seconds }
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [stage, onStageChange])

  // Progress calculation
  useEffect(() => {
    let targetProgress = 0
    switch (stage) {
      case 'pre-cooking':
        targetProgress = 20
        break
      case 'cooking':
        targetProgress = 60
        break
      case 'delivery':
        targetProgress = 90
        break
    }
    setProgress(targetProgress)
  }, [stage])

  const getStageIcon = () => {
    switch (stage) {
      case 'pre-cooking':
        return <Clock size={32} className="text-gray-400" />
      case 'cooking':
        return <ChefHat size={32} className="text-primary-500" />
      case 'delivery':
        return <Rocket size={32} className="text-yellow-400" />
    }
  }

  const getStageMessage = () => {
    switch (stage) {
      case 'pre-cooking':
        return 'Editing will be unavailable 30 minutes before cooking'
      case 'cooking':
        return 'Cooking...'
      case 'delivery':
        return 'On the way...'
    }
  }

  const [meal, setMeal] = useState<Meal | null>(null)
  const [loading, setLoading] = useState(true)

  // Récupérer le repas en cours depuis le backend
  useEffect(() => {
    const fetchCurrentMeal = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/api/current-meal`)
        if (response.ok) {
          const data = await response.json()
          setMeal(data)
        }
      } catch (err) {
        console.error('Erreur chargement repas:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchCurrentMeal()
  }, [stage])

  return (
    <div className="p-4">
      {/* Stage Icon */}
      <div className="icon-container">
        {getStageIcon()}
      </div>

      {/* Timer */}
      <div className="timer">
        {timeLeft.hours}h : {timeLeft.minutes}m : {timeLeft.seconds}s
      </div>

      {/* Progress Bar */}
      <div className="progress-bar mb-4">
        <div 
          className="progress-fill"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Stage Message */}
      <p className="text-center text-gray-400 text-sm mb-6">
        {getStageMessage()}
      </p>

      {/* Meal Card */}
      <div className="mb-6">
        {loading ? (
          <div className="text-center py-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-500 mx-auto"></div>
            <p className="text-gray-400 mt-2 text-sm">Chargement...</p>
          </div>
        ) : meal ? (
          <MealCard meal={{...meal, time: meal.time || '09:00'}} />
        ) : (
          <div className="text-center py-4">
            <p className="text-gray-400">Aucun repas en cours</p>
          </div>
        )}
      </div>

      {/* Map for delivery stage */}
      {stage === 'delivery' && (
        <div className="bg-dark-800 rounded-xl p-4 h-48 flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center mb-2 mx-auto">
              <Rocket size={24} className="text-white" />
            </div>
            <p className="text-sm text-gray-400">Delivery tracking map</p>
            <p className="text-xs text-gray-500 mt-1">Route visualization coming soon</p>
          </div>
        </div>
      )}
    </div>
  )
}

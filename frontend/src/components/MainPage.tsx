'use client'

import { useState, useEffect } from 'react'
import { Bike, Edit3 } from 'lucide-react'
import MealCard from './MealCard'
import DatePicker from './DatePicker'
import { useMeals } from '@/hooks/useMeals'
import { useCurrentMeal } from '@/hooks/useCurrentMeal'

interface MainPageProps {
  selectedDate: number
  onDateChange: (date: number) => void
  selectedPlanId?: number | null
}

export default function MainPage({ selectedDate, onDateChange, selectedPlanId }: MainPageProps) {
  const [isScrolled, setIsScrolled] = useState(false)
  
  // Utiliser les hooks pour gérer les données
  const { meals, loading, error, updateMeal, refetch } = useMeals(selectedPlanId)
  const { currentMeal, loading: currentMealLoading } = useCurrentMeal()

  const handleToggleFavorite = async (mealId: number) => {
    // Cette fonction sera gérée par le composant MealCard
    await refetch() // Rafraîchir après modification
  }

  const handleRate = async (mealId: number, rating: number) => {
    await updateMeal(mealId, { rating })
  }

  return (
    <div className="relative">
      {/* Hero Section avec style Jow */}
      <div className="px-2 sm:px-4 md:px-6 lg:px-8 xl:px-12">
        <div className="max-w-7xl mx-auto">
          <div className="hero-container">
            <div className="hero-title">🍽️ JowCameroun Dîners</div>
            <div className="hero-subtitle">
              Planifie tes dîners de la semaine avec des recettes camerounaises authentiques 🇨🇲✨
            </div>
          </div>
        </div>
      </div>

      {/* Layout principal - responsive */}
      <div className="px-2 sm:px-4 md:px-6 lg:px-8 xl:px-12 2xl:px-16">
        <div className="max-w-8xl mx-auto">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8 xl:gap-12 2xl:gap-16">
            {/* Colonne gauche - Date Picker */}
            <div className="lg:col-span-4 xl:col-span-3">
              {/* Date Picker */}
              <div className="py-4">
                <DatePicker 
                  selectedDate={selectedDate} 
                  onDateChange={onDateChange}
                />
              </div>
            </div>

            {/* Colonne centre - Repas planifiés */}
            <div className="lg:col-span-5 xl:col-span-6">
              <div className="meal-card-grid">
        {loading && (
          <div className="col-span-full text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
            <p className="text-brown-600 mt-2">Chargement des repas...</p>
          </div>
        )}
        
        {error && (
          <div className="col-span-full text-center py-8">
            <p className="text-red-500">{error}</p>
            <button 
              onClick={() => window.location.reload()}
              className="btn-primary mt-2 px-4 py-2"
            >
              Réessayer
            </button>
          </div>
        )}
        
        {!loading && !error && meals.length === 0 && (
          <div className="col-span-full text-center py-12">
            <div className="max-w-md mx-auto">
              <div className="text-6xl mb-4">🍽️</div>
              <h3 className="text-xl font-semibold text-brown-900 mb-2">Aucun repas planifié</h3>
              <p className="text-brown-600 mb-6">Pour cette date, vous n'avez pas encore de repas prévu. Créez votre premier repas !</p>
              <button className="btn-primary px-6 py-3 text-lg font-semibold">
                Planifier un repas
              </button>
            </div>
          </div>
        )}
        
        {!loading && !error && meals.map((meal) => (
          <MealCard 
            key={meal.id} 
            meal={meal}
            onToggleFavorite={handleToggleFavorite}
            onRate={handleRate}
            planId={selectedPlanId}
          />
        ))}
              </div>
            </div>

            {/* Colonne droite - Repas actuel en cours */}
            <div className="lg:col-span-3 xl:col-span-3">
              {/* Repas actuel en cours de préparation */}
              {currentMeal && !currentMealLoading && (
                <div className="mt-6 lg:mt-0">
                  <h3 className="text-brown-900 text-lg font-semibold mb-3 font-display">🍳 En cours de préparation</h3>
                  <MealCard 
                    meal={currentMeal}
                    onToggleFavorite={handleToggleFavorite}
                    onRate={handleRate}
                    planId={selectedPlanId}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

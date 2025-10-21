'use client'

import { BarChart3, TrendingUp, Star, ChefHat, Heart } from 'lucide-react'
import { useStatistics } from '@/hooks/useStatistics'

export default function StatisticsPage() {
  const { statistics, loading, error } = useStatistics()

  if (loading) {
    return (
      <div className="p-4">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
          <p className="text-gray-400 mt-2">Chargement des statistiques...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4">
        <div className="text-center py-8">
          <p className="text-red-400">{error}</p>
        </div>
      </div>
    )
  }

  if (!statistics) {
    return (
      <div className="p-4">
        <div className="text-center py-8">
          <p className="text-gray-400">Aucune donnée disponible</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 lg:p-8">
      <h1 className="text-2xl lg:text-3xl font-bold mb-6 flex items-center font-display">
        <BarChart3 className="mr-2 text-primary-500" size={24} />
        Mes Statistiques de Dîners
      </h1>

      {/* Métriques principales */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="metric-card">
          <div className="flex items-center justify-between mb-2">
            <ChefHat className="text-primary-500" size={20} />
            <span className="text-2xl font-bold text-brown-900">{statistics.totalPlans}</span>
          </div>
          <p className="text-sm text-brown-600">Plans créés</p>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="text-green-500" size={20} />
            <span className="text-2xl font-bold text-brown-900">{statistics.totalRecipes}</span>
          </div>
          <p className="text-sm text-brown-600">Recettes</p>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between mb-2">
            <Heart className="text-red-500" size={20} />
            <span className="text-2xl font-bold text-brown-900">{statistics.favoriteRecipes}</span>
          </div>
          <p className="text-sm text-brown-600">Favoris</p>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between mb-2">
            <Star className="text-yellow-500" size={20} />
            <span className="text-2xl font-bold text-brown-900">{statistics.avgRating}/5</span>
          </div>
          <p className="text-sm text-brown-600">Note moyenne</p>
        </div>
      </div>

      {/* Ingrédients préférés */}
      {statistics.topIngredients && statistics.topIngredients.length > 0 && (
        <div className="metric-card mb-6">
          <h2 className="text-lg font-semibold text-brown-900 mb-4 flex items-center font-display">
            <ChefHat className="mr-2 text-primary-500" size={20} />
            Ingrédients Préférés
          </h2>
          
          <div className="space-y-3">
            {statistics.topIngredients.map(([ingredient, count], index) => (
              <div key={ingredient} className="flex items-center justify-between">
                <div className="flex items-center">
                  <span className="text-sm text-brown-500 w-6">#{index + 1}</span>
                  <span className="text-brown-900 font-medium capitalize">{ingredient}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-brown-200 rounded-full h-2">
                    <div 
                      className="bg-gradient-primary h-2 rounded-full transition-all duration-300"
                      style={{ 
                        width: `${Math.min(100, (count / Math.max(...statistics.topIngredients.map(([, c]) => c))) * 100)}%` 
                      }}
                    />
                  </div>
                  <span className="text-sm text-brown-600 w-8 text-right">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Graphiques et insights */}
      <div className="metric-card">
        <h2 className="text-lg font-semibold text-brown-900 mb-4 font-display">
          Insights
        </h2>
        
        <div className="space-y-3 text-sm">
          <div className="flex items-center justify-between p-3 bg-cream-100 rounded-lg">
            <span className="text-brown-700">Recettes par plan en moyenne</span>
            <span className="text-brown-900 font-medium">
              {statistics.totalPlans > 0 ? Math.round(statistics.totalRecipes / statistics.totalPlans) : 0}
            </span>
          </div>
          
          <div className="flex items-center justify-between p-3 bg-cream-100 rounded-lg">
            <span className="text-brown-700">Taux de favoris</span>
            <span className="text-brown-900 font-medium">
              {statistics.totalRecipes > 0 ? Math.round((statistics.favoriteRecipes / statistics.totalRecipes) * 100) : 0}%
            </span>
          </div>
          
          <div className="flex items-center justify-between p-3 bg-cream-100 rounded-lg">
            <span className="text-brown-700">Diversité culinaire</span>
            <span className="text-brown-900 font-medium">
              {statistics.topIngredients?.length || 0} ingrédients différents
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

'use client'

import { Heart, Star, Clock, ChefHat } from 'lucide-react'
import { useFavorites } from '@/hooks/useFavorites'

export default function FavoritesPage() {
  const { favorites, loading, error, refetch } = useFavorites()

  return (
    <div className="p-4 lg:p-8">
      <h1 className="text-2xl lg:text-3xl font-bold mb-6 flex items-center font-display">
        <Heart className="mr-2 text-primary-500" size={24} />
        Mes Favoris
      </h1>
      
      {loading && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
          <p className="text-brown-600 mt-2">Chargement des favoris...</p>
        </div>
      )}
      
      {error && (
        <div className="text-center py-8">
          <p className="text-red-500">{error}</p>
          <button 
            onClick={refetch}
            className="btn-primary mt-2 px-4 py-2"
          >
            Réessayer
          </button>
        </div>
      )}
      
      {!loading && !error && favorites.length === 0 && (
        <div className="text-center py-8">
          <Heart className="mx-auto text-brown-400 mb-4" size={48} />
          <p className="text-brown-600">Aucun favori pour le moment</p>
        </div>
      )}
      
      <div className="meal-card-grid">
        {!loading && !error && favorites.map((favorite) => (
          <div key={favorite.id} className="meal-card">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-brown-900 font-semibold text-lg font-display">
                {favorite.name}
              </h3>
              <div className="flex items-center space-x-1">
                <Heart size={20} className="text-red-500 fill-current" />
                {favorite.rating && favorite.rating > 0 && (
                  <div className="flex items-center space-x-1">
                    <Star size={16} className="text-yellow-400 fill-current" />
                    <span className="text-sm text-brown-500">{favorite.rating}/5</span>
                  </div>
                )}
              </div>
            </div>
            
            <p className="text-brown-600 text-sm mb-2">
              {favorite.ingredient} • {favorite.cuisine}
            </p>
            
            <div className="flex items-center space-x-4 text-xs text-brown-500">
              {favorite.prepTime && (
                <div className="flex items-center space-x-1">
                  <Clock size={12} />
                  <span>Prép: {favorite.prepTime}m</span>
                </div>
              )}
              {favorite.cookTime && (
                <div className="flex items-center space-x-1">
                  <ChefHat size={12} />
                  <span>Cuisson: {favorite.cookTime}m</span>
                </div>
              )}
            </div>
            
            {favorite.notes && (
              <p className="text-sm text-brown-700 mt-2 italic">"{favorite.notes}"</p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

'use client'

import { useState } from 'react'
import { Play, Globe, ExternalLink } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import Image from 'next/image'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'

// Données de démonstration pour les recettes Jow
const demoJowMeals = [
  {
    id: 1,
    name: "Riz Coco & Mangue",
    image: "https://static.jow.fr/recipes/YXAbXJPROwkh0w.png",
    videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ", // URL de démonstration
    url: "https://jow.fr/recipes/61c9964ec5541a0ede3e92a7",
    jowId: "61c9964ec5541a0ede3e92a7",
    cuisine: "asiatique",
    ingredient: "Mangue",
    prepTime: 2,
    cookTime: 35,
    rating: 4,
    isFavorite: false
  },
  {
    id: 2,
    name: "Rouleaux de printemps à la crevette",
    image: "https://static.jow.fr/recipes/example2.png",
    videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ", // URL de démonstration
    url: "https://jow.fr/recipes/example2",
    jowId: "example2",
    cuisine: "asiatique",
    ingredient: "Crevette",
    prepTime: 15,
    cookTime: 10,
    rating: 5,
    isFavorite: true
  }
]

export default function JowDemo() {
  const [showVideo, setShowVideo] = useState<number | null>(null)

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Démonstration des Recettes Jow</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {demoJowMeals.map((meal) => (
          <Card key={meal.id} className="overflow-hidden">
            {/* Image avec overlay */}
            <div className="relative h-48 overflow-hidden">
              <Image 
                src={meal.image} 
                alt={meal.name}
                fill
                className="object-cover"
                unoptimized={true} // Désactiver l'optimisation pour les images Jow
              />
              
              {/* Badge Jow */}
              <div className="absolute top-3 left-3">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-500 text-white">
                  🌍 Jow
                </span>
              </div>

              {/* Badge favori */}
              {meal.isFavorite && (
                <div className="absolute top-3 right-3">
                  <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm">❤️</span>
                  </div>
                </div>
              )}

              {/* Overlay avec actions */}
              <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-40 transition-all duration-300 flex items-center justify-center opacity-0 hover:opacity-100">
                <div className="flex space-x-2">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setShowVideo(showVideo === meal.id ? null : meal.id)}
                    className="bg-white bg-opacity-90 hover:bg-opacity-100"
                  >
                    <Play size={16} />
                  </Button>
                  
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => window.open(meal.url, '_blank')}
                    className="bg-white bg-opacity-90 hover:bg-opacity-100"
                  >
                    <Globe size={16} />
                  </Button>
                  
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => console.log('Voir détails:', meal.name)}
                    className="bg-white bg-opacity-90 hover:bg-opacity-100"
                  >
                    <ExternalLink size={16} />
                  </Button>
                </div>
              </div>
            </div>

            <CardContent className="p-4">
              <CardHeader className="p-0 mb-3">
                <CardTitle className="text-lg">{meal.name}</CardTitle>
                <div className="flex items-center justify-between text-sm text-gray-600">
                  <span>Dîner - 19:00</span>
                  <span className="text-orange-600">🥘 {meal.ingredient}</span>
                </div>
              </CardHeader>

              {/* Métriques */}
              <div className="grid grid-cols-2 gap-2 mb-3">
                <div className="flex items-center text-sm text-gray-600">
                  <span>⏱️ Prép: {meal.prepTime}m</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <span>👨‍🍳 Cuisson: {meal.cookTime}m</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <span>🔥 500 kcal</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <span>⭐ {meal.rating}/5</span>
                </div>
              </div>

              {/* Section vidéo */}
              <AnimatePresence>
                {showVideo === meal.id && meal.videoUrl && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mb-3 p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <p className="text-sm font-medium text-gray-700">Vidéo de la recette:</p>
                      <button
                        onClick={() => setShowVideo(null)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        ✕
                      </button>
                    </div>
                    <div className="relative w-full h-48 bg-black rounded-lg overflow-hidden">
                      <iframe
                        src={meal.videoUrl}
                        className="w-full h-full"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                        title={`Vidéo de ${meal.name}`}
                      />
                    </div>
                    <div className="mt-2">
                      <a
                        href={meal.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
                      >
                        <Globe size={14} className="mr-1" />
                        Voir la recette complète sur Jow.fr
                      </a>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Actions */}
              <div className="flex space-x-2">
                <Button
                  size="sm"
                  variant="outline"
                  className="flex-1"
                >
                  Ajouter au plan
                </Button>
                
                <Button
                  size="sm"
                  variant="primary"
                  className="flex-1"
                >
                  Voir détails
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

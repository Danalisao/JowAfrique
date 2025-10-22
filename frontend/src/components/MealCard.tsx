'use client'

import { useState } from 'react'
import { Heart, Star, Clock, ChefHat, ExternalLink, Edit3, Plus, Play, Globe, Sparkles, MessageSquare } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import Image from 'next/image'
import { Meal } from '@/types'
import { useFavorites } from '@/hooks/useFavorites'
import { useMeals } from '@/hooks/useMeals'
import { useMealActions } from '@/hooks/useMealActions'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import StarRating from '@/components/ui/StarRating'
import MealVariations from '@/components/MealVariations'
import { cn, getMealTypeIcon, getCuisineIcon, calculateCalories, calculateWeight } from '@/lib/utils'

interface MealCardProps {
  meal: Meal
  onEdit?: (meal: Meal) => void
  onToggleFavorite?: (mealId: number) => void
  onRate?: (mealId: number, rating: number) => void
  planId?: number | null
  variant?: 'default' | 'compact' | 'featured'
}

export default function MealCard({ 
  meal, 
  onEdit, 
  onToggleFavorite, 
  onRate, 
  planId, 
  variant = 'default' 
}: MealCardProps) {
  const [isHovered, setIsHovered] = useState(false)
  const [showRating, setShowRating] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [showVideo, setShowVideo] = useState(false)
  const [showVariations, setShowVariations] = useState(false)
  const [showNotes, setShowNotes] = useState(false)
  const [notes, setNotes] = useState(meal.notes || '')
  
  const { addFavorite, removeFavorite } = useFavorites()
  const { updateMeal } = useMeals(planId)
  const { rateMeal, addNotes } = useMealActions()

  const handleToggleFavorite = async () => {
    setIsLoading(true)
    if (meal.isFavorite) {
      await removeFavorite(meal.id)
    } else {
      await addFavorite(meal.id)
    }
    if (onToggleFavorite) {
      onToggleFavorite(meal.id)
    }
    setIsLoading(false)
  }

  const handleRate = async (rating: number) => {
    const success = await rateMeal(meal.id, rating)
    if (success && onRate) {
      onRate(meal.id, rating)
    }
    setShowRating(false)
  }

  const handleSaveNotes = async () => {
    const success = await addNotes(meal.id, notes)
    if (success) {
      setShowNotes(false)
    }
  }

  const handleAddToPlan = () => {
    // Logique pour ajouter à un plan de dîners
    // Note: Fonctionnalité à implémenter dans une future version
  }

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.3, ease: "easeOut" }
    },
    hover: { 
      y: -4,
      transition: { duration: 0.2, ease: "easeOut" }
    }
  }

  const imageVariants = {
    hover: { scale: 1.05 },
    tap: { scale: 0.95 }
  }

  if (variant === 'compact') {
    return (
      <motion.div
        variants={cardVariants}
        initial="hidden"
        animate="visible"
        whileHover="hover"
        className="flex items-center space-x-3 p-3 bg-white rounded-lg border border-gray-200 hover:border-orange-200 hover:shadow-md transition-all duration-200 w-full"
      >
        <div className="flex-shrink-0 relative">
          {meal.image ? (
            <Image 
              src={meal.image} 
              alt={meal.name}
              width={48}
              height={48}
              className="rounded-lg object-cover"
              unoptimized={meal.jowId ? true : false} // Désactiver l'optimisation pour les images Jow
            />
          ) : (
            <div className="w-12 h-12 rounded-lg bg-orange-100 flex items-center justify-center">
              <ChefHat size={20} className="text-orange-500" />
            </div>
          )}
          {/* Badge Jow pour version compacte */}
          {meal.jowId && (
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
              <span className="text-xs text-white">🌍</span>
            </div>
          )}
        </div>
        
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-medium text-gray-900 truncate">{meal.name}</h4>
          <p className="text-xs text-gray-500">{meal.type}</p>
        </div>
        
        <div className="flex items-center space-x-1">
          {meal.rating && meal.rating > 0 && (
            <div className="flex items-center">
              <Star size={12} className="text-yellow-400 fill-current" />
              <span className="text-xs text-gray-600 ml-1">{meal.rating}</span>
            </div>
          )}
          <button
            onClick={handleToggleFavorite}
            disabled={isLoading}
            className={cn(
              "p-1 rounded-full transition-colors",
              meal.isFavorite 
                ? "text-red-500 hover:text-red-600" 
                : "text-gray-400 hover:text-red-500"
            )}
          >
            <Heart size={14} fill={meal.isFavorite ? 'currentColor' : 'none'} />
          </button>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="group"
    >
      <Card 
        className={cn(
          "overflow-hidden transition-all duration-300 w-full",
          variant === 'featured' && "ring-2 ring-orange-200 shadow-lg"
        )}
        hover={true}
        clickable={true}
      >
        {/* Image avec overlay */}
        <div className="relative h-52 overflow-hidden rounded-t-2xl">
          {meal.image ? (
            <motion.div
              variants={imageVariants}
              whileHover="hover"
              whileTap="tap"
              className="w-full h-full"
            >
              <Image 
                src={meal.image} 
                alt={meal.name}
                fill
                className="object-cover"
                unoptimized={meal.jowId ? true : false} // Désactiver l'optimisation pour les images Jow
              />
            </motion.div>
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-orange-50 via-orange-100 to-orange-200 flex items-center justify-center">
              <div className="text-center">
                <ChefHat size={48} className="text-orange-400 mx-auto mb-2" />
                <p className="text-orange-600 text-sm font-medium">Image à venir</p>
              </div>
            </div>
          )}
          
          {/* Overlay avec actions */}
          <AnimatePresence>
            {isHovered && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent flex items-center justify-center"
              >
                <div className="flex space-x-2">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={handleToggleFavorite}
                    disabled={isLoading}
                    className="bg-white/90 hover:bg-white backdrop-blur-sm shadow-lg"
                  >
                    <Heart 
                      size={16} 
                      fill={meal.isFavorite ? 'currentColor' : 'none'} 
                      className={meal.isFavorite ? 'text-red-500' : ''}
                    />
                  </Button>
                  
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setShowRating(!showRating)}
                    className="bg-white/90 hover:bg-white backdrop-blur-sm shadow-lg"
                  >
                    <Star size={16} />
                  </Button>
                  
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setShowVariations(!showVariations)}
                    className="bg-white/90 hover:bg-white backdrop-blur-sm shadow-lg"
                  >
                    <Sparkles size={16} />
                  </Button>
                  
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setShowNotes(!showNotes)}
                    className="bg-white/90 hover:bg-white backdrop-blur-sm shadow-lg"
                  >
                    <MessageSquare size={16} />
                  </Button>
                  
                  {/* Bouton vidéo pour les recettes Jow */}
                  {meal.videoUrl && (
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => setShowVideo(!showVideo)}
                      className="bg-white/90 hover:bg-white backdrop-blur-sm shadow-lg"
                    >
                      <Play size={16} />
                    </Button>
                  )}
                  
                  {/* Bouton lien Jow */}
                  {meal.url && (
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => window.open(meal.url, '_blank')}
                      className="bg-white/90 hover:bg-white backdrop-blur-sm shadow-lg"
                    >
                      <Globe size={16} />
                    </Button>
                  )}
                  
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => {/* Voir détails - à implémenter */}}
                    className="bg-white/90 hover:bg-white backdrop-blur-sm shadow-lg"
                  >
                    <ExternalLink size={16} />
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Badge cuisine */}
          {meal.cuisine && (
            <div className="absolute top-3 left-3">
              <span className="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-medium bg-white/95 backdrop-blur-sm text-gray-900 shadow-lg border border-white/20">
                {getCuisineIcon(meal.cuisine)} {meal.cuisine}
              </span>
            </div>
          )}

          {/* Badge Jow */}
          {meal.jowId && (
            <div className="absolute top-3 left-3">
              <span className="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-medium bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg">
                🌍 Jow
              </span>
            </div>
          )}

          {/* Badge favori */}
          {meal.isFavorite && (
            <div className="absolute top-3 right-3">
              <div className="w-8 h-8 bg-gradient-to-r from-red-500 to-pink-500 rounded-full flex items-center justify-center shadow-lg">
                <Heart size={16} className="text-white fill-current" />
              </div>
            </div>
          )}

          {/* Bouton d'édition */}
          {meal.isEditable && onEdit && (
            <div className="absolute top-3 right-3">
              <Button
                size="sm"
                variant="ghost"
                onClick={() => onEdit(meal)}
                className="bg-white bg-opacity-90 hover:bg-opacity-100"
              >
                <Edit3 size={16} />
              </Button>
            </div>
          )}
        </div>

        <CardContent className="p-4">
          <CardHeader className="p-0 mb-3">
            <div className="flex items-start justify-between">
              <CardTitle className="text-lg leading-tight">{meal.name}</CardTitle>
              <span className="text-2xl">{getMealTypeIcon(meal.type)}</span>
            </div>
            
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>{meal.type} {meal.time && `- ${meal.time}`}</span>
              {meal.ingredient && (
                <span className="text-orange-600">🥘 {meal.ingredient}</span>
              )}
            </div>
          </CardHeader>

          {/* Métriques */}
          <div className="grid grid-cols-2 gap-2 mb-3">
            {meal.prepTime && (
              <div className="flex items-center text-sm text-gray-600">
                <Clock size={14} className="mr-1" />
                <span>Prép: {meal.prepTime}m</span>
              </div>
            )}
            {meal.cookTime && (
              <div className="flex items-center text-sm text-gray-600">
                <ChefHat size={14} className="mr-1" />
                <span>Cuisson: {meal.cookTime}m</span>
              </div>
            )}
            <div className="flex items-center text-sm text-gray-600">
              <span>🔥 {meal.calories}</span>
            </div>
            {meal.weight && (
              <div className="flex items-center text-sm text-gray-600">
                <span>⚖️ {meal.weight}</span>
              </div>
            )}
          </div>

          {/* Rating existant */}
          {meal.rating && meal.rating > 0 && (
            <div className="flex items-center mb-3">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    size={14}
                    className={i < meal.rating! ? 'text-yellow-400 fill-current' : 'text-gray-300'}
                  />
                ))}
              </div>
              <span className="text-sm text-gray-600 ml-2">({meal.rating}/5)</span>
            </div>
          )}

          {/* Rating selector */}
          <AnimatePresence>
            {showRating && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-3 p-3 bg-gray-50 rounded-lg"
              >
                <p className="text-sm font-medium text-gray-700 mb-2">Noter cette recette:</p>
                <div className="flex space-x-1">
                  {[1, 2, 3, 4, 5].map((rating) => (
                    <button
                      key={rating}
                      onClick={() => handleRate(rating)}
                      disabled={isLoading}
                      className={cn(
                        "p-1 rounded transition-colors",
                        meal.rating === rating 
                          ? "text-yellow-400 bg-yellow-50" 
                          : "text-gray-300 hover:text-yellow-400"
                      )}
                    >
                      <Star size={18} fill={meal.rating === rating ? 'currentColor' : 'none'} />
                    </button>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Section vidéo Jow */}
          <AnimatePresence>
            {showVideo && meal.videoUrl && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-3 p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-700">Vidéo de la recette:</p>
                  <button
                    onClick={() => setShowVideo(false)}
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
                {meal.url && (
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
                )}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Section notation améliorée */}
          <AnimatePresence>
            {showRating && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-3 p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-700">Noter cette recette:</p>
                  <button
                    onClick={() => setShowRating(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                <StarRating 
                  rating={meal.rating || 0} 
                  onRate={handleRate}
                  size="lg"
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Section notes */}
          <AnimatePresence>
            {showNotes && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-3 p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-700">Notes personnelles:</p>
                  <button
                    onClick={() => setShowNotes(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Ajoutez vos notes sur cette recette..."
                  className="w-full p-2 border border-gray-300 rounded-md text-sm resize-none"
                  rows={3}
                />
                <div className="flex justify-end mt-2">
                  <Button
                    size="sm"
                    onClick={handleSaveNotes}
                    className="bg-blue-500 hover:bg-blue-600 text-white"
                  >
                    Sauvegarder
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Section variations IA */}
          <AnimatePresence>
            {showVariations && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-3"
              >
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-700">Variations IA</p>
                  <button
                    onClick={() => setShowVariations(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                <MealVariations 
                  mealId={meal.id}
                  currentMealName={meal.name}
                  onSelectVariation={(variation) => {
                    // Variation sélectionnée - logique à implémenter
                    setShowVariations(false)
                  }}
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Notes existantes */}
          {meal.notes && (
            <div className="flex items-start text-sm text-gray-600 mb-3">
              <Edit3 size={14} className="mr-2 mt-0.5 flex-shrink-0" />
              <span>{meal.notes}</span>
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
            <Button
              size="sm"
              variant="outline"
              onClick={handleAddToPlan}
              className="flex-1 w-full sm:w-auto"
            >
              <Plus size={14} className="mr-1" />
              <span className="hidden xs:inline">Ajouter</span>
              <span className="xs:hidden">+</span>
            </Button>
            
            <Button
              size="sm"
              variant="primary"
              onClick={() => {/* Voir détails - à implémenter */}}
              className="flex-1 w-full sm:w-auto"
            >
              <span className="hidden xs:inline">Voir détails</span>
              <span className="xs:hidden">Détails</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}
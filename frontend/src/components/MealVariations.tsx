'use client'

import { useState, useEffect } from 'react'
import { Sparkles, ChefHat, Clock, Users } from 'lucide-react'
import { useAiFeatures } from '@/hooks/useAiFeatures'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

interface MealVariationsProps {
  mealId: number
  currentMealName: string
  onSelectVariation?: (variation: any) => void
}

export default function MealVariations({ 
  mealId, 
  currentMealName, 
  onSelectVariation 
}: MealVariationsProps) {
  const { getVariations, loading, error } = useAiFeatures()
  const [variations, setVariations] = useState<any[]>([])
  const [showVariations, setShowVariations] = useState(false)

  const loadVariations = async () => {
    const result = await getVariations(mealId)
    if (result) {
      setVariations(result)
      setShowVariations(true)
    }
  }

  return (
    <div className="space-y-4">
      <Button
        onClick={loadVariations}
        disabled={loading}
        className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white"
      >
        <Sparkles className="w-4 h-4 mr-2" />
        {loading ? 'Génération des variations...' : 'Variations IA'}
      </Button>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {showVariations && variations.length > 0 && (
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-800">
            Variations suggérées pour "{currentMealName}"
          </h4>
          
          {variations.map((variation, index) => (
            <Card key={index} className="p-4 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h5 className="font-medium text-gray-900 mb-2">
                    {variation.name}
                  </h5>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                    {variation.prepTime && (
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        {variation.prepTime}min
                      </div>
                    )}
                    {variation.servings && (
                      <div className="flex items-center">
                        <Users className="w-4 h-4 mr-1" />
                        {variation.servings} personnes
                      </div>
                    )}
                  </div>
                  
                  <p className="text-gray-700 text-sm mb-3">
                    {variation.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-2">
                    {variation.ingredients?.map((ingredient: string, idx: number) => (
                      <span 
                        key={idx}
                        className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs"
                      >
                        {ingredient}
                      </span>
                    ))}
                  </div>
                </div>
                
                <Button
                  onClick={() => onSelectVariation?.(variation)}
                  className="ml-4 bg-blue-500 hover:bg-blue-600 text-white text-sm"
                >
                  <ChefHat className="w-4 h-4 mr-1" />
                  Choisir
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {showVariations && variations.length === 0 && (
        <div className="text-center py-4 text-gray-500">
          <Sparkles className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p>Aucune variation trouvée pour ce repas</p>
        </div>
      )}
    </div>
  )
}

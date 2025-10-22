'use client'

import { useState } from 'react'
import { Activity, Zap, Heart, Apple, Target } from 'lucide-react'
import { useAiFeatures } from '@/hooks/useAiFeatures'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

interface NutritionAnalysisProps {
  planId: number
}

export default function NutritionAnalysis({ planId }: NutritionAnalysisProps) {
  const { analyzePlanNutrition, loading, error } = useAiFeatures()
  const [analysis, setAnalysis] = useState<any>(null)
  const [showAnalysis, setShowAnalysis] = useState(false)

  const loadAnalysis = async () => {
    const result = await analyzePlanNutrition(planId)
    if (result) {
      setAnalysis(result)
      setShowAnalysis(true)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  return (
    <div className="space-y-4">
      <Button
        onClick={loadAnalysis}
        disabled={loading}
        className="w-full bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white"
      >
        <Activity className="w-4 h-4 mr-2" />
        {loading ? 'Analyse en cours...' : 'Analyse Nutritionnelle IA'}
      </Button>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {showAnalysis && analysis && (
        <div className="space-y-4">
          <Card className="p-4">
            <h4 className="font-semibold text-gray-800 mb-4 flex items-center">
              <Apple className="w-5 h-5 mr-2 text-green-600" />
              Score Nutritionnel Global
            </h4>
            
            <div className={`rounded-lg p-4 ${getScoreBg(analysis.overallScore)}`}>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Score</span>
                <span className={`text-2xl font-bold ${getScoreColor(analysis.overallScore)}`}>
                  {analysis.overallScore}/100
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className={`h-2 rounded-full ${
                    analysis.overallScore >= 80 ? 'bg-green-500' :
                    analysis.overallScore >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${analysis.overallScore}%` }}
                ></div>
              </div>
            </div>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="p-4">
              <h5 className="font-medium text-gray-800 mb-3 flex items-center">
                <Zap className="w-4 h-4 mr-2 text-yellow-600" />
                Macronutriments
              </h5>
              <div className="space-y-2">
                {analysis.macronutrients?.map((macro: any, index: number) => (
                  <div key={index} className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">{macro.name}</span>
                    <span className="text-sm font-medium">{macro.value}</span>
                  </div>
                ))}
              </div>
            </Card>

            <Card className="p-4">
              <h5 className="font-medium text-gray-800 mb-3 flex items-center">
                <Heart className="w-4 h-4 mr-2 text-red-600" />
                Micronutriments
              </h5>
              <div className="space-y-2">
                {analysis.micronutrients?.map((micro: any, index: number) => (
                  <div key={index} className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">{micro.name}</span>
                    <span className="text-sm font-medium">{micro.value}</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {analysis.recommendations && analysis.recommendations.length > 0 && (
            <Card className="p-4">
              <h5 className="font-medium text-gray-800 mb-3 flex items-center">
                <Target className="w-4 h-4 mr-2 text-blue-600" />
                Recommandations IA
              </h5>
              <ul className="space-y-2">
                {analysis.recommendations.map((rec: string, index: number) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </Card>
          )}

          {analysis.healthBenefits && analysis.healthBenefits.length > 0 && (
            <Card className="p-4">
              <h5 className="font-medium text-gray-800 mb-3 flex items-center">
                <Heart className="w-4 h-4 mr-2 text-green-600" />
                Bénéfices Santé
              </h5>
              <ul className="space-y-2">
                {analysis.healthBenefits.map((benefit: string, index: number) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    {benefit}
                  </li>
                ))}
              </ul>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}

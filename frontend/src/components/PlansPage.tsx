'use client'

import { useState } from 'react'
import { Calendar, Plus, Trash2, ChefHat, Clock, Sparkles, Activity, ShoppingCart } from 'lucide-react'
import { usePlans } from '@/hooks/usePlans'
import { useMeals } from '@/hooks/useMeals'
import { useShoppingList } from '@/hooks/useShoppingList'
import { useAiFeatures } from '@/hooks/useAiFeatures'
import { UserPreferences } from '@/types'
import { Button } from '@/components/ui/Button'
import NutritionAnalysis from '@/components/NutritionAnalysis'

interface PlansPageProps {
  onSelectPlan?: (planId: number) => void
  selectedPlanId?: number | null
}

export default function PlansPage({ onSelectPlan, selectedPlanId }: PlansPageProps) {
  const { plans, loading, error, createPlan, removePlan } = usePlans()
  const { meals } = useMeals(selectedPlanId ?? null)
  const { ingredients, loading: shoppingLoading, generateList } = useShoppingList()
  const { generatePlanWithAi, optimizeShopping } = useAiFeatures()
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [showShoppingList, setShowShoppingList] = useState(false)
  const [showNutritionAnalysis, setShowNutritionAnalysis] = useState(false)
  const [showAiCreateForm, setShowAiCreateForm] = useState(false)

  const handleCreatePlan = async (formData: FormData) => {
    const planName = formData.get('planName') as string
    const weekStartDate = formData.get('weekStartDate') as string
    const cuisines = formData.getAll('cuisines') as string[]
    const budget = formData.get('budget') as string
    const light = formData.get('light') === 'on'
    const vegetarian = formData.get('vegetarian') === 'on'

    const preferences: UserPreferences = {
      cuisines,
      budget: budget as 'économique' | 'modéré' | 'cher',
      light,
      vegetarian
    }

    const newPlan = await createPlan({
      planName,
      weekStartDate,
      preferences
    })

    if (newPlan) {
      setShowCreateForm(false)
      if (onSelectPlan) {
        onSelectPlan(newPlan.id)
      }
    }
  }

  const handleCreateAiPlan = async (formData: FormData) => {
    const planName = formData.get('planName') as string
    const weekStartDate = formData.get('weekStartDate') as string
    const cuisines = formData.getAll('cuisines') as string[]
    const budget = formData.get('budget') as string
    const light = formData.get('light') === 'on'
    const vegetarian = formData.get('vegetarian') === 'on'

    const preferences: UserPreferences = {
      cuisines,
      budget: budget as 'économique' | 'modéré' | 'cher',
      light,
      vegetarian
    }

    const newPlan = await generatePlanWithAi({
      planName,
      weekStartDate,
      preferences
    })

    if (newPlan) {
      setShowAiCreateForm(false)
      if (onSelectPlan) {
        onSelectPlan(newPlan.id)
      }
    }
  }

  const handleOptimizeShopping = async () => {
    if (selectedPlanId) {
      await optimizeShopping(selectedPlanId, 50) // Budget par défaut de 50€
    }
  }

  const handleGenerateShoppingList = async (planId: number) => {
    await generateList(planId)
    setShowShoppingList(true)
  }

  if (showShoppingList && ingredients.length > 0) {
    return (
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold flex items-center font-display">
            <ChefHat className="mr-2 text-primary-500" size={24} />
            Liste de Courses
          </h1>
          <button
            onClick={() => setShowShoppingList(false)}
            className="text-brown-600 hover:text-brown-900"
          >
            ← Retour
          </button>
        </div>

        <div className="space-y-2">
          {ingredients.map((ingredient, index) => (
            <div key={index} className="meal-card flex items-center">
              <input type="checkbox" className="mr-3 text-primary-500" />
              <span className="text-brown-900">{ingredient}</span>
            </div>
          ))}
        </div>

        <div className="mt-6 flex space-x-3">
          <button className="btn-primary flex-1 py-2 px-4">
            Copier la liste
          </button>
          <button className="btn-secondary flex-1 py-2 px-4">
            Partager
          </button>
        </div>
      </div>
    )
  }

  if (showCreateForm) {
    return (
      <div className="p-4 lg:p-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl lg:text-3xl font-bold flex items-center font-display">
            <Plus className="mr-2 text-primary-500" size={24} />
            Nouveau Plan
          </h1>
          <button
            onClick={() => setShowCreateForm(false)}
            className="text-brown-600 hover:text-brown-900"
          >
            ← Retour
          </button>
        </div>

        <div className="max-w-2xl mx-auto">
          <form action={handleCreatePlan} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-brown-700 mb-2">
              Nom du plan
            </label>
            <input
              type="text"
              name="planName"
              required
              className="w-full bg-white text-brown-900 border border-brown-200 rounded-lg px-3 py-2 focus:border-primary-500 focus:outline-none"
              placeholder="Ex: Plan de la semaine du 15 janvier"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-brown-700 mb-2">
              Date de début
            </label>
            <input
              type="date"
              name="weekStartDate"
              required
              className="w-full bg-white text-brown-900 border border-brown-200 rounded-lg px-3 py-2 focus:border-primary-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-brown-700 mb-2">
              Cuisines préférées
            </label>
            <div className="space-y-2">
              {['cameroun', 'asiatique', 'mexican', 'french'].map((cuisine) => (
                <label key={cuisine} className="flex items-center">
                  <input
                    type="checkbox"
                    name="cuisines"
                    value={cuisine}
                    defaultChecked={cuisine === 'cameroun' || cuisine === 'asiatique'}
                    className="mr-2 text-primary-500 focus:ring-primary-500"
                  />
                  <span className="text-brown-700 capitalize">{cuisine}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-brown-700 mb-2">
              Budget
            </label>
            <select
              name="budget"
              className="w-full bg-white text-brown-900 border border-brown-200 rounded-lg px-3 py-2 focus:border-primary-500 focus:outline-none"
            >
              <option value="économique">Économique</option>
              <option value="modéré" selected>Modéré</option>
              <option value="cher">Cher</option>
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="flex items-center">
              <input type="checkbox" name="light" defaultChecked className="mr-2 text-primary-500 focus:ring-primary-500" />
              <span className="text-brown-700">Plats légers</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" name="vegetarian" className="mr-2 text-primary-500 focus:ring-primary-500" />
              <span className="text-brown-700">Végétarien</span>
            </label>
          </div>

          <button
            type="submit"
            className="btn-primary w-full py-3 px-4 font-semibold"
          >
            Créer le plan
          </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 lg:p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl lg:text-3xl font-bold flex items-center font-display">
          <Calendar className="mr-2 text-primary-500" size={24} />
          Mes Plans de Dîners
        </h1>
        <button
          onClick={() => setShowCreateForm(true)}
          className="btn-primary p-2 rounded-lg"
        >
          <Plus size={20} />
        </button>
      </div>

      {loading && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
          <p className="text-brown-600 mt-2">Chargement des plans...</p>
        </div>
      )}

      {error && (
        <div className="text-center py-8">
          <p className="text-red-500">{error}</p>
        </div>
      )}

      {!loading && !error && plans.length === 0 && (
        <div className="text-center py-8">
          <Calendar className="mx-auto text-brown-400 mb-4" size={48} />
          <p className="text-brown-600">Aucun plan créé</p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="btn-primary mt-2 px-4 py-2"
          >
            Créer un plan
          </button>
        </div>
      )}

      <div className="meal-card-grid">
        {!loading && !error && plans.map((plan) => (
          <div key={plan.id} className="meal-card">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="text-brown-900 font-semibold text-lg font-display">
                  {plan.planName}
                </h3>
                <p className="text-brown-600 text-sm">
                  Semaine du {new Date(plan.weekStartDate).toLocaleDateString('fr-FR')}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleGenerateShoppingList(plan.id)}
                  className="text-brown-400 hover:text-primary-500"
                  title="Liste de courses"
                >
                  <ChefHat size={16} />
                </button>
                <button
                  onClick={() => setShowNutritionAnalysis(!showNutritionAnalysis)}
                  className="text-brown-400 hover:text-green-500"
                  title="Analyse nutritionnelle"
                >
                  <Activity size={16} />
                </button>
                <button
                  onClick={() => handleOptimizeShopping()}
                  className="text-brown-400 hover:text-purple-500"
                  title="Optimiser liste de courses"
                >
                  <Sparkles size={16} />
                </button>
                <button
                  onClick={() => removePlan(plan.id)}
                  className="text-brown-400 hover:text-red-500"
                  title="Supprimer"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>

            <div className="flex items-center space-x-4 text-xs text-brown-500 mb-3">
              <span>Budget: {plan.totalBudgetEstimate || 'N/A'}€</span>
              <span>IA: {plan.generatedByAi ? 'Oui' : 'Non'}</span>
              <span>Créé: {new Date(plan.createdAt).toLocaleDateString('fr-FR')}</span>
            </div>

            {selectedPlanId === plan.id && meals.length > 0 && (
              <div className="mt-3 pt-3 border-t border-brown-200">
                <h4 className="text-brown-900 font-medium mb-2">Repas planifiés:</h4>
                <div className="space-y-1">
                  {meals.slice(0, 3).map((meal) => (
                    <div key={meal.id} className="flex items-center text-sm text-brown-700">
                      <Clock size={12} className="mr-2" />
                      <span>{meal.dayOfWeek} - {meal.name}</span>
                    </div>
                  ))}
                  {meals.length > 3 && (
                    <p className="text-xs text-brown-500">+{meals.length - 3} autres repas</p>
                  )}
                </div>
              </div>
            )}

            <button
              onClick={() => onSelectPlan?.(plan.id)}
              className={`w-full mt-3 py-2 px-4 rounded-lg text-sm font-medium ${
                selectedPlanId === plan.id 
                  ? 'bg-green-500 text-white' 
                  : 'btn-primary'
              }`}
            >
              {selectedPlanId === plan.id ? 'Plan sélectionné' : 'Sélectionner ce plan'}
            </button>
          </div>
        ))}
      </div>

      {/* Boutons de création de plan */}
      <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
        <Button
          onClick={() => setShowCreateForm(true)}
          className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-medium"
        >
          <Plus className="w-5 h-5 mr-2" />
          Créer un Plan Manuel
        </Button>
        
        <Button
          onClick={() => setShowAiCreateForm(true)}
          className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-6 py-3 rounded-lg font-medium"
        >
          <Sparkles className="w-5 h-5 mr-2" />
          Générer avec l'IA
        </Button>
      </div>

      {/* Section analyse nutritionnelle */}
      {showNutritionAnalysis && selectedPlanId && (
        <div className="mt-8 p-6 bg-white rounded-lg shadow-md">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-green-600" />
              Analyse Nutritionnelle
            </h3>
            <button
              onClick={() => setShowNutritionAnalysis(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
          <NutritionAnalysis planId={selectedPlanId} />
        </div>
      )}

      {/* Formulaire de création de plan IA */}
      {showAiCreateForm && (
        <div className="mt-8 p-6 bg-white rounded-lg shadow-md">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center">
              <Sparkles className="w-5 h-5 mr-2 text-purple-600" />
              Créer un Plan avec l'IA
            </h3>
            <button
              onClick={() => setShowAiCreateForm(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
          
          <form action={handleCreateAiPlan} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nom du plan
              </label>
              <input
                type="text"
                name="planName"
                required
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Plan IA Cameroun"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date de début
              </label>
              <input
                type="date"
                name="weekStartDate"
                required
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cuisines préférées
              </label>
              <div className="flex flex-wrap gap-2">
                {['cameroun', 'asiatique', 'mexican', 'french'].map((cuisine) => (
                  <label key={cuisine} className="flex items-center">
                    <input
                      type="checkbox"
                      name="cuisines"
                      value={cuisine}
                      defaultChecked={cuisine === 'cameroun'}
                      className="mr-2"
                    />
                    <span className="text-sm capitalize">{cuisine}</span>
                  </label>
                ))}
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Budget
              </label>
              <select
                name="budget"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="économique">Économique</option>
                <option value="modéré" selected>Modéré</option>
                <option value="cher">Cher</option>
              </select>
            </div>
            
            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input type="checkbox" name="light" className="mr-2" />
                <span className="text-sm">Repas légers</span>
              </label>
              <label className="flex items-center">
                <input type="checkbox" name="vegetarian" className="mr-2" />
                <span className="text-sm">Végétarien</span>
              </label>
            </div>
            
            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white py-3 rounded-lg font-medium"
            >
              <Sparkles className="w-5 h-5 mr-2" />
              Générer le Plan avec l'IA
            </Button>
          </form>
        </div>
      )}
    </div>
  )
}

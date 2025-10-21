'use client'

import { useState, useEffect } from 'react'
import { Settings, User, Bell, Shield } from 'lucide-react'

export default function SettingsPage() {
  const [statistics, setStatistics] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/api/statistics`)
        if (response.ok) {
          const data = await response.json()
          setStatistics(data)
        }
      } catch (err) {
        console.error('Erreur chargement stats:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchStatistics()
  }, [])

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6 flex items-center">
        <Settings className="mr-2 text-primary-500" size={24} />
        Paramètres
      </h1>
      
      {/* Statistiques */}
      {statistics && (
        <div className="bg-dark-800 rounded-xl p-4 mb-6">
          <h2 className="text-lg font-semibold mb-4">Mes Statistiques</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-500">{statistics.totalPlans}</div>
              <div className="text-sm text-gray-400">Plans créés</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-500">{statistics.totalRecipes}</div>
              <div className="text-sm text-gray-400">Recettes</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-500">{statistics.favoriteRecipes}</div>
              <div className="text-sm text-gray-400">Favoris</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-500">{statistics.avgRating}/5</div>
              <div className="text-sm text-gray-400">Note moyenne</div>
            </div>
          </div>
        </div>
      )}
      
      {/* Options */}
      <div className="space-y-4">
        <div className="bg-dark-800 rounded-xl p-4 flex items-center">
          <User className="mr-3 text-primary-500" size={20} />
          <div>
            <div className="font-semibold">Profil</div>
            <div className="text-sm text-gray-400">Gérer votre compte</div>
          </div>
        </div>
        
        <div className="bg-dark-800 rounded-xl p-4 flex items-center">
          <Bell className="mr-3 text-primary-500" size={20} />
          <div>
            <div className="font-semibold">Notifications</div>
            <div className="text-sm text-gray-400">Alertes et rappels</div>
          </div>
        </div>
        
        <div className="bg-dark-800 rounded-xl p-4 flex items-center">
          <Shield className="mr-3 text-primary-500" size={20} />
          <div>
            <div className="font-semibold">Confidentialité</div>
            <div className="text-sm text-gray-400">Données et sécurité</div>
          </div>
        </div>
      </div>
    </div>
  )
}

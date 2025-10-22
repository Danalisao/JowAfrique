'use client'

import { Calendar, Heart, BarChart3, Settings, Utensils, ChefHat } from 'lucide-react'

interface DesktopNavigationProps {
  activeTab: 'home' | 'progress' | 'favorites' | 'settings' | 'cart' | 'plans' | 'statistics'
  onTabChange: (tab: 'home' | 'progress' | 'favorites' | 'settings' | 'cart' | 'plans' | 'statistics') => void
}

export default function DesktopNavigation({ activeTab, onTabChange }: DesktopNavigationProps) {
  const navItems = [
    { id: 'home', icon: Utensils, label: 'Accueil', description: 'Vue d\'ensemble' },
    { id: 'plans', icon: Calendar, label: 'Plans', description: 'Gestion des plans' },
    { id: 'favorites', icon: Heart, label: 'Favoris', description: 'Recettes préférées' },
    { id: 'statistics', icon: BarChart3, label: 'Statistiques', description: 'Analyses et stats' },
    { id: 'settings', icon: Settings, label: 'Réglages', description: 'Configuration' },
  ]

  return (
    <div className="desktop-nav">
      {/* Logo/Header */}
      <div className="p-6 border-b border-brown-200/50 bg-gradient-to-r from-white to-warm-white">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center shadow-lg">
            <ChefHat className="w-7 h-7 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-brown-900 font-display">JowCameroun</h1>
            <p className="text-sm text-brown-600 font-medium">Planificateur</p>
          </div>
        </div>
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map(({ id, icon: Icon, label, description }) => (
          <button
            key={id}
            onClick={() => onTabChange(id as any)}
            className={`w-full flex items-center space-x-3 p-4 rounded-xl transition-all duration-300 ${
              activeTab === id
                ? 'bg-gradient-primary text-white shadow-lg transform scale-105'
                : 'text-brown-700 hover:bg-gradient-to-r hover:from-orange-50 hover:to-orange-100 hover:text-brown-900 hover:shadow-md'
            }`}
          >
            <Icon size={20} />
            <div className="flex-1 text-left">
              <div className="font-medium">{label}</div>
              <div className={`text-xs ${activeTab === id ? 'text-white/80' : 'text-brown-500'}`}>
                {description}
              </div>
            </div>
          </button>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-brown-200">
        <div className="text-xs text-brown-500 text-center">
          Version 1.0.0
        </div>
      </div>
    </div>
  )
}

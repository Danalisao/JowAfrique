'use client'

import { Plus, Utensils, Heart, Settings, ShoppingCart, Calendar, BarChart3 } from 'lucide-react'

interface BottomNavigationProps {
  activeTab: 'home' | 'progress' | 'favorites' | 'settings' | 'cart' | 'plans' | 'statistics'
  onTabChange: (tab: 'home' | 'progress' | 'favorites' | 'settings' | 'cart' | 'plans' | 'statistics') => void
}

export default function BottomNavigation({ activeTab, onTabChange }: BottomNavigationProps) {
  const navItems = [
    { id: 'home', icon: Utensils, label: 'Accueil' },
    { id: 'plans', icon: Calendar, label: 'Plans' },
    { id: 'favorites', icon: Heart, label: 'Favoris' },
    { id: 'statistics', icon: BarChart3, label: 'Stats' },
    { id: 'settings', icon: Settings, label: 'Réglages' },
  ]

  return (
    <div className="bottom-nav">
      <div className="flex justify-around">
        {navItems.map(({ id, icon: Icon, label }) => (
          <button
            key={id}
            onClick={() => onTabChange(id as any)}
            className={`nav-item ${activeTab === id ? 'active' : ''}`}
          >
            <Icon size={20} />
            <span className="mt-1">{label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

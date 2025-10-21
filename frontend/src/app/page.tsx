'use client'

import { useState } from 'react'
import StatusBar from '@/components/StatusBar'
import BottomNavigation from '@/components/BottomNavigation'
import DesktopNavigation from '@/components/DesktopNavigation'
import MainPage from '@/components/MainPage'
import ProgressPage from '@/components/ProgressPage'
import FavoritesPage from '@/components/FavoritesPage'
import SettingsPage from '@/components/SettingsPage'
import CartPage from '@/components/CartPage'
import PlansPage from '@/components/PlansPage'
import StatisticsPage from '@/components/StatisticsPage'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'home' | 'progress' | 'favorites' | 'settings' | 'cart' | 'plans' | 'statistics'>('home')
  const [selectedDate, setSelectedDate] = useState(2) // Mardi - pour les dîners
  const [progressStage, setProgressStage] = useState<'pre-cooking' | 'cooking' | 'delivery'>('pre-cooking')
  const [selectedPlanId, setSelectedPlanId] = useState<number | null>(1)

  return (
    <div className="min-h-screen" style={{ background: 'var(--light-cream)' }}>
      {/* Desktop Navigation */}
      <DesktopNavigation activeTab={activeTab} onTabChange={setActiveTab} />
      
      {/* Mobile Status Bar */}
      <div className="lg:hidden">
        <StatusBar />
      </div>
      
      <main className="desktop-main pb-20 lg:pb-0">
        {activeTab === 'home' && (
          <MainPage 
            selectedDate={selectedDate} 
            onDateChange={setSelectedDate}
            selectedPlanId={selectedPlanId}
          />
        )}
        
        {activeTab === 'progress' && (
          <ProgressPage 
            stage={progressStage}
            onStageChange={setProgressStage}
          />
        )}
        
        {activeTab === 'favorites' && (
          <FavoritesPage />
        )}
        
        {activeTab === 'plans' && (
          <PlansPage 
            onSelectPlan={setSelectedPlanId}
            selectedPlanId={selectedPlanId}
          />
        )}
        
        {activeTab === 'statistics' && (
          <StatisticsPage />
        )}
        
        {activeTab === 'settings' && (
          <SettingsPage />
        )}
        
        {activeTab === 'cart' && (
          <CartPage />
        )}
      </main>
      
      {/* Mobile Bottom Navigation */}
      <div className="lg:hidden">
        <BottomNavigation 
          activeTab={activeTab} 
          onTabChange={setActiveTab}
        />
      </div>
    </div>
  )
}

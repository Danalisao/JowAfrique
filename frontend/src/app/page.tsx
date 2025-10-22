'use client'

import { useApp } from '@/providers/AppContext'
import { NAVIGATION_TABS } from '@/lib/constants'
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

// Mapping des pages par onglet
const PAGES = {
  [NAVIGATION_TABS.HOME]: MainPage,
  [NAVIGATION_TABS.PROGRESS]: ProgressPage,
  [NAVIGATION_TABS.FAVORITES]: FavoritesPage,
  [NAVIGATION_TABS.SETTINGS]: SettingsPage,
  [NAVIGATION_TABS.CART]: CartPage,
  [NAVIGATION_TABS.PLANS]: PlansPage,
  [NAVIGATION_TABS.STATISTICS]: StatisticsPage,
} as const

/**
 * Page principale (root layout)
 * Utilise le contexte global pour l'état et affiche la page appropriée
 */
export default function Home() {
  const { activeTab, selectedDate, onDateChange, selectedPlanId, onSelectPlan, progressStage, onProgressStageChange } = useApp()

  // Récupère le composant de page approprié
  const CurrentPage = PAGES[activeTab]

  // Props dynamiques selon la page
  const getPageProps = () => {
    switch (activeTab) {
      case NAVIGATION_TABS.HOME:
        return {
          selectedDate,
          onDateChange,
          selectedPlanId,
        }
      case NAVIGATION_TABS.PROGRESS:
        return {
          stage: progressStage,
          onStageChange: onProgressStageChange,
        }
      case NAVIGATION_TABS.PLANS:
        return {
          onSelectPlan,
          selectedPlanId,
        }
      default:
        return {}
    }
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--light-cream)' }}>
      {/* Desktop Navigation */}
      <DesktopNavigation activeTab={activeTab} onTabChange={useApp().setActiveTab} />

      {/* Mobile Status Bar */}
      <div className="lg:hidden">
        <StatusBar />
      </div>

      <main className="desktop-main pb-20 lg:pb-0">
        <CurrentPage {...getPageProps()} />
      </main>

      {/* Mobile Bottom Navigation */}
      <div className="lg:hidden">
        <BottomNavigation activeTab={activeTab} onTabChange={useApp().setActiveTab} />
      </div>
    </div>
  )
}

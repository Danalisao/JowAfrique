'use client'

import React, { createContext, useContext, useState, useCallback } from 'react'
import { NAVIGATION_TABS, PROGRESS_STAGES, DEFAULT_VALUES } from '@/lib/constants'
import type { NavigationTab, ProgressStage } from '@/lib/constants'

interface AppContextType {
  // Navigation
  activeTab: NavigationTab
  setActiveTab: (tab: NavigationTab) => void

  // Plans
  selectedPlanId: number | null
  setSelectedPlanId: (id: number | null) => void

  // Dates
  selectedDate: number
  setSelectedDate: (date: number) => void

  // Progress
  progressStage: ProgressStage
  setProgressStage: (stage: ProgressStage) => void
}

const AppContext = createContext<AppContextType | undefined>(undefined)

/**
 * Provider pour l'état global de l'application
 * Centralise tous les états utilisés par les pages
 */
export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeTab, setActiveTab] = useState<NavigationTab>(NAVIGATION_TABS.HOME)
  const [selectedPlanId, setSelectedPlanId] = useState<number | null>(DEFAULT_VALUES.SELECTED_PLAN_ID)
  const [selectedDate, setSelectedDate] = useState<number>(DEFAULT_VALUES.SELECTED_DATE)
  const [progressStage, setProgressStage] = useState<ProgressStage>(PROGRESS_STAGES.PRE_COOKING)

  const value: AppContextType = {
    activeTab,
    setActiveTab,
    selectedPlanId,
    setSelectedPlanId,
    selectedDate,
    setSelectedDate,
    progressStage,
    setProgressStage,
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

/**
 * Hook pour utiliser le contexte global
 * À utiliser dans tous les composants qui ont besoin d'accéder à l'état global
 */
export const useApp = (): AppContextType => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp doit être utilisé dans un AppProvider')
  }
  return context
}

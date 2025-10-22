'use client'

import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'

interface DatePickerProps {
  selectedDate: number
  onDateChange: (date: number) => void
}

export default function DatePicker({ selectedDate, onDateChange }: DatePickerProps) {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [showMonthPicker, setShowMonthPicker] = useState(false)

  // Générer les 7 prochains jours à partir d'aujourd'hui (pour les dîners)
  const generateWeekDates = () => {
    const dates = []
    const today = new Date()
    
    for (let i = 0; i < 7; i++) {
      const date = new Date(today)
      date.setDate(today.getDate() + i)
      dates.push({
        date: date.getDate(),
        day: date.getDay(),
        fullDate: date,
        label: date.toLocaleDateString('fr-FR', { weekday: 'short' }),
        isToday: i === 0,
        isSelected: selectedDate === date.getDate()
      })
    }
    
    return dates
  }

  const weekDates = generateWeekDates()

  const formatMonthYear = (date: Date) => {
    return date.toLocaleDateString('fr-FR', { 
      month: 'long', 
      year: 'numeric' 
    }).replace(/^\w/, c => c.toUpperCase())
  }

  const navigateWeek = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate)
    newDate.setDate(currentDate.getDate() + (direction === 'next' ? 7 : -7))
    setCurrentDate(newDate)
  }

  return (
    <div className="w-full">
      {/* Version mobile - horizontale */}
      <div className="block md:hidden">
        <div className="flex items-center justify-center mb-3">
          <button
            onClick={() => navigateWeek('prev')}
            className="p-1 rounded-full hover:bg-gray-100 transition-colors mr-4"
          >
            <ChevronLeft size={16} className="text-brown-600" />
          </button>
          
          <span className="text-brown-900 font-medium text-sm">
            {formatMonthYear(currentDate)}
          </span>
          
          <button
            onClick={() => navigateWeek('next')}
            className="p-1 rounded-full hover:bg-gray-100 transition-colors ml-4"
          >
            <ChevronRight size={16} className="text-brown-600" />
          </button>
        </div>

        <div className="flex space-x-3 overflow-x-auto pb-2 justify-center">
          {weekDates.map((dateInfo, index) => (
            <button
              key={index}
              onClick={() => onDateChange(dateInfo.date)}
              className={`date-item flex-shrink-0 ${dateInfo.isSelected ? 'active' : ''} ${
                dateInfo.isToday ? 'today' : ''
              }`}
            >
              <div className="text-center">
                <div className="text-sm font-medium">{dateInfo.date}</div>
                <div className="text-xs opacity-70">{dateInfo.label}</div>
              </div>
            </button>
          ))}
        </div>
        
        {/* Indicateur de semaine mobile */}
        <div className="mt-3 text-center">
          <span className="text-xs text-brown-500 bg-brown-50 px-2 py-1 rounded-full">
            Semaine du {weekDates[0].fullDate.toLocaleDateString('fr-FR', { 
              day: 'numeric', 
              month: 'short' 
            })} au {weekDates[6].fullDate.toLocaleDateString('fr-FR', { 
              day: 'numeric', 
              month: 'short' 
            })}
          </span>
        </div>
      </div>

      {/* Version desktop - grille */}
      <div className="hidden md:block">
        {/* En-tête avec navigation */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={() => navigateWeek('prev')}
            className="p-3 rounded-full hover:bg-gray-100 transition-colors"
          >
            <ChevronLeft size={24} className="text-brown-600" />
          </button>
          
          <button
            onClick={() => setShowMonthPicker(!showMonthPicker)}
            className="text-brown-900 font-medium text-lg hover:text-primary-500 transition-colors"
          >
            {formatMonthYear(currentDate)}
          </button>
          
          <button
            onClick={() => navigateWeek('next')}
            className="p-3 rounded-full hover:bg-gray-100 transition-colors"
          >
            <ChevronRight size={24} className="text-brown-600" />
          </button>
        </div>

        {/* Grille des dates */}
        <div className="grid grid-cols-7 gap-2 sm:gap-4 md:gap-6 xl:gap-8">
          {weekDates.map((dateInfo, index) => (
            <button
              key={index}
              onClick={() => onDateChange(dateInfo.date)}
              className={`date-item-desktop ${dateInfo.isSelected ? 'active' : ''} ${
                dateInfo.isToday ? 'today' : ''
              }`}
            >
              <div className="text-center">
                <div className="text-base font-medium">{dateInfo.date}</div>
                <div className="text-sm opacity-70">{dateInfo.label}</div>
              </div>
            </button>
          ))}
        </div>

        {/* Indicateur de semaine actuelle */}
        <div className="mt-4 text-center">
          <span className="text-sm text-brown-500 bg-brown-50 px-3 py-2 rounded-full">
            Semaine du {weekDates[0].fullDate.toLocaleDateString('fr-FR', { 
              day: 'numeric', 
              month: 'short' 
            })} au {weekDates[6].fullDate.toLocaleDateString('fr-FR', { 
              day: 'numeric', 
              month: 'short' 
            })}
          </span>
        </div>
      </div>
    </div>
  )
}

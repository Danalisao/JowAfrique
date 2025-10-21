import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleDateString('fr-FR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

export function formatTime(time: string): string {
  return time.slice(0, 5) // HH:MM format
}

export function getMealTypeIcon(mealType: string): string {
  switch (mealType.toLowerCase()) {
    case 'petit-déjeuner':
      return '🌅'
    case 'déjeuner':
      return '🍽️'
    case 'dîner':
      return '🌙'
    default:
      return '🍴'
  }
}

export function getCuisineIcon(cuisine: string): string {
  switch (cuisine.toLowerCase()) {
    case 'cameroun':
      return '🇨🇲'
    case 'asiatique':
      return '🍜'
    case 'mexican':
      return '🌮'
    case 'french':
      return '🥖'
    default:
      return '🌍'
  }
}

export function calculateCalories(prepTime?: number, cookTime?: number): string {
  if (!prepTime || !cookTime) return "N/A"
  const calories = prepTime * 10 + cookTime * 5
  return `${calories} kcal`
}

export function calculateWeight(prepTime?: number): string {
  if (!prepTime) return "N/A"
  return `${prepTime * 15} gm`
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

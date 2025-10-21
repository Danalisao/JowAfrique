'use client'

import { useState, useEffect, useCallback, useMemo } from 'react'
import { debounce } from '@/lib/utils'

interface SearchResult<T> {
  item: T
  score: number
  highlights: string[]
}

interface SearchOptions<T> {
  keys: (keyof T)[]
  threshold?: number
  includeScore?: boolean
  includeMatches?: boolean
  minMatchCharLength?: number
}

export function useSearch<T>(
  items: T[],
  options: SearchOptions<T>
) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult<T>[]>([])
  const [isSearching, setIsSearching] = useState(false)

  const {
    keys,
    threshold = 0.6,
    includeScore = true,
    includeMatches = true,
    minMatchCharLength = 2
  } = options

  // Simple fuzzy search implementation
  const searchItems = useCallback((searchQuery: string, itemsToSearch: T[]): SearchResult<T>[] => {
    if (!searchQuery || searchQuery.length < minMatchCharLength) {
      return []
    }

    const normalizedQuery = searchQuery.toLowerCase().trim()
    const results: SearchResult<T>[] = []

    for (const item of itemsToSearch) {
      let bestScore = 0
      const highlights: string[] = []

      for (const key of keys) {
        const value = item[key]
        if (typeof value === 'string') {
          const normalizedValue = value.toLowerCase()
          const score = calculateScore(normalizedQuery, normalizedValue)
          
          if (score > bestScore) {
            bestScore = score
          }

          if (score > 0) {
            highlights.push(highlightMatch(value, normalizedQuery))
          }
        }
      }

      if (bestScore >= threshold) {
        results.push({
          item,
          score: bestScore,
          highlights: [...new Set(highlights)]
        })
      }
    }

    return results.sort((a, b) => b.score - a.score)
  }, [keys, threshold, minMatchCharLength])

  // Debounced search
  const debouncedSearch = useMemo(
    () => debounce((searchQuery: string) => {
      setIsSearching(true)
      const searchResults = searchItems(searchQuery, items)
      setResults(searchResults)
      setIsSearching(false)
    }, 300),
    [searchItems, items]
  )

  // Update search when query changes
  useEffect(() => {
    if (query) {
      debouncedSearch(query)
    } else {
      setResults([])
      setIsSearching(false)
    }
  }, [query, debouncedSearch])

  const clearSearch = useCallback(() => {
    setQuery('')
    setResults([])
    setIsSearching(false)
  }, [])

  return {
    query,
    setQuery,
    results,
    isSearching,
    clearSearch,
    hasResults: results.length > 0
  }
}

// Simple scoring algorithm
function calculateScore(query: string, text: string): number {
  if (query === text) return 1.0
  if (text.includes(query)) return 0.8
  if (text.startsWith(query)) return 0.9

  // Levenshtein distance based scoring
  const distance = levenshteinDistance(query, text)
  const maxLength = Math.max(query.length, text.length)
  return maxLength === 0 ? 0 : (maxLength - distance) / maxLength
}

// Simple Levenshtein distance implementation
function levenshteinDistance(str1: string, str2: string): number {
  const matrix = Array(str2.length + 1).fill(null).map(() => Array(str1.length + 1).fill(null))

  for (let i = 0; i <= str1.length; i++) matrix[0][i] = i
  for (let j = 0; j <= str2.length; j++) matrix[j][0] = j

  for (let j = 1; j <= str2.length; j++) {
    for (let i = 1; i <= str1.length; i++) {
      const indicator = str1[i - 1] === str2[j - 1] ? 0 : 1
      matrix[j][i] = Math.min(
        matrix[j][i - 1] + 1,
        matrix[j - 1][i] + 1,
        matrix[j - 1][i - 1] + indicator
      )
    }
  }

  return matrix[str2.length][str1.length]
}

// Highlight matching text
function highlightMatch(text: string, query: string): string {
  const regex = new RegExp(`(${query})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

// Hook for meal search
export function useMealSearch(meals: any[]) {
  return useSearch(meals, {
    keys: ['name', 'ingredient', 'cuisine'],
    threshold: 0.3,
    includeScore: true,
    includeMatches: true,
    minMatchCharLength: 2
  })
}

// Hook for plan search
export function usePlanSearch(plans: any[]) {
  return useSearch(plans, {
    keys: ['planName'],
    threshold: 0.4,
    includeScore: true,
    includeMatches: true,
    minMatchCharLength: 2
  })
}

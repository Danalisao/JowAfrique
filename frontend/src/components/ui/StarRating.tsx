'use client'

import { useState } from 'react'
import { Star } from 'lucide-react'

interface StarRatingProps {
  rating: number
  onRate: (rating: number) => void
  readOnly?: boolean
  size?: 'sm' | 'md' | 'lg'
}

export default function StarRating({ 
  rating, 
  onRate, 
  readOnly = false, 
  size = 'md' 
}: StarRatingProps) {
  const [hoverRating, setHoverRating] = useState(0)
  
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  }
  
  const handleClick = (rating: number) => {
    if (!readOnly) {
      onRate(rating)
    }
  }
  
  return (
    <div className="flex items-center space-x-1">
      {[1, 2, 3, 4, 5].map((star) => {
        const isActive = star <= (hoverRating || rating)
        return (
          <button
            key={star}
            type="button"
            disabled={readOnly}
            onClick={() => handleClick(star)}
            onMouseEnter={() => !readOnly && setHoverRating(star)}
            onMouseLeave={() => !readOnly && setHoverRating(0)}
            className={`${sizeClasses[size]} transition-colors ${
              readOnly ? 'cursor-default' : 'cursor-pointer hover:scale-110'
            }`}
          >
            <Star
              className={`${
                isActive 
                  ? 'text-yellow-400 fill-yellow-400' 
                  : 'text-gray-300'
              } transition-colors`}
            />
          </button>
        )
      })}
      {!readOnly && (
        <span className="text-sm text-gray-500 ml-2">
          {hoverRating || rating}/5
        </span>
      )}
    </div>
  )
}

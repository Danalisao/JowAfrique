"""
Modèles de données pour JowAfrique
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class MealType(Enum):
    BREAKFAST = "Petit-déjeuner"
    LUNCH = "Déjeuner"
    DINNER = "Dîner"

class CuisineType(Enum):
    CAMEROUN = "cameroun"
    ASIATIQUE = "asiatique"
    MEXICAN = "mexican"
    FRENCH = "french"

class BudgetLevel(Enum):
    ECONOMIC = "économique"
    MODERATE = "modéré"
    EXPENSIVE = "cher"

@dataclass
class Meal:
    id: Optional[int]
    day_of_week: str
    meal_type: MealType
    recipe_name: str
    jow_recipe_id: Optional[str] = None
    jow_recipe_url: Optional[str] = None
    main_ingredient: Optional[str] = None
    cuisine_type: Optional[CuisineType] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    is_favorite: bool = False
    rating: int = 0
    notes: Optional[str] = None
    plan_id: Optional[int] = None

@dataclass
class WeeklyPlan:
    id: Optional[int]
    plan_name: str
    week_start_date: date
    total_budget_estimate: Optional[float] = None
    generated_by_ai: bool = True
    created_at: Optional[datetime] = None

@dataclass
class UserPreferences:
    cuisines: List[CuisineType]
    budget: BudgetLevel
    light: bool = False
    vegetarian: bool = False

@dataclass
class Statistics:
    total_plans: int
    total_recipes: int
    favorite_recipes: int
    avg_rating: float
    top_ingredients: List[tuple[str, int]]

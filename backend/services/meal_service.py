"""
Service de gestion des repas
"""
from typing import List, Optional, Dict, Any
from models import Meal, MealType, CuisineType
from database import DatabaseManager

class MealService:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_meals_by_plan(self, plan_id: int) -> List[Dict[str, Any]]:
        """Récupère tous les repas d'un plan"""
        return self.db.get_plan_meals(plan_id)
    
    def get_current_meal(self, day_of_week: str = "Mardi") -> Optional[Dict[str, Any]]:
        """Récupère le repas actuel (par défaut Mardi)"""
        # Logique pour déterminer le repas actuel
        # Pour l'instant, on prend le premier repas du jour
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, day_of_week, meal_type, recipe_name, jow_recipe_id, 
                       jow_recipe_url, main_ingredient, cuisine_type, image_url, 
                       video_url, prep_time, cook_time, is_favorite, rating, notes
                FROM meal_slots
                WHERE day_of_week = ? AND meal_type = 'Déjeuner'
                LIMIT 1
            """, (day_of_week,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def add_meal(self, meal_data: Dict[str, Any]) -> int:
        """Ajoute un nouveau repas"""
        meal = Meal(
            id=None,
            day_of_week=meal_data.get('day_of_week'),
            meal_type=MealType(meal_data.get('meal_type', 'Dîner')),
            recipe_name=meal_data['recipe_name'],
            jow_recipe_id=meal_data.get('jow_recipe_id'),
            jow_recipe_url=meal_data.get('jow_recipe_url'),
            main_ingredient=meal_data.get('main_ingredient'),
            cuisine_type=CuisineType(meal_data['cuisine_type']) if meal_data.get('cuisine_type') else None,
            image_url=meal_data.get('image_url'),
            video_url=meal_data.get('video_url'),
            prep_time=meal_data.get('prep_time'),
            cook_time=meal_data.get('cook_time'),
            is_favorite=meal_data.get('is_favorite', False),
            rating=meal_data.get('rating', 0),
            notes=meal_data.get('notes'),
            plan_id=meal_data.get('plan_id')
        )
        
        # Si pas de plan_id, ajouter comme recette de base
        if meal.plan_id is None:
            return self.db.add_base_recipe(meal)
        else:
            return self.db.add_meal_to_plan(meal)
    
    def update_meal(self, meal_id: int, updates: Dict[str, Any]) -> bool:
        """Met à jour un repas"""
        return self.db.update_meal(meal_id, updates)
    
    def toggle_favorite(self, meal_id: int) -> bool:
        """Bascule le statut favori d'un repas"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_favorite FROM meal_slots WHERE id = ?", (meal_id,))
            row = cursor.fetchone()
            if row:
                new_favorite = not row[0]
                return self.db.update_meal(meal_id, {'is_favorite': new_favorite})
        return False
    
    def rate_meal(self, meal_id: int, rating: int) -> bool:
        """Note un repas (1-5)"""
        if 1 <= rating <= 5:
            return self.db.update_meal(meal_id, {'rating': rating})
        return False
    
    def add_notes(self, meal_id: int, notes: str) -> bool:
        """Ajoute des notes à un repas"""
        return self.db.update_meal(meal_id, {'notes': notes})
    
    def generate_shopping_list(self, plan_id: int) -> List[str]:
        """Génère une liste de courses pour un plan"""
        meals = self.get_meals_by_plan(plan_id)
        ingredients = set()
        
        for meal in meals:
            if meal['main_ingredient']:
                ingredients.add(meal['main_ingredient'])
            
            # Ajouter des ingrédients communs selon la cuisine
            cuisine = meal.get('cuisine_type')
            if cuisine == 'cameroun':
                ingredients.update([
                    'oignons', 'tomates', 'ail', 'gingembre', 'huile de palme',
                    'piment', 'cubes maggi', 'plantain', 'taro', 'arachide',
                    'feuilles vertes', 'poisson fumé'
                ])
            elif cuisine == 'asiatique':
                ingredients.update([
                    'sauce soja', 'gingembre', 'ail', 'oignons verts',
                    'huile de sésame', 'nouilles de riz', 'tofu', 'lait de coco',
                    'curry', 'pousses de soja', 'carottes', 'brocolis'
                ])
            elif cuisine == 'mexican':
                ingredients.update(['avocat', 'lime', 'coriandre', 'fromage', 'tortillas'])
        
        return list(ingredients)

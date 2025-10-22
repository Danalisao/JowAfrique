"""
Service de gestion des plans hebdomadaires avec génération IA
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from models import WeeklyPlan, UserPreferences, CuisineType, BudgetLevel, Meal, MealType
from database import DatabaseManager

class PlanService:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_plan(self, plan_name: str, week_start_date: date, 
                   preferences: UserPreferences, budget: Optional[float] = None) -> int:
        """Crée un nouveau plan hebdomadaire"""
        plan = WeeklyPlan(
            id=None,
            plan_name=plan_name,
            week_start_date=week_start_date,
            total_budget_estimate=budget,
            generated_by_ai=False,
            created_at=datetime.now()
        )
        return self.db.create_plan(plan)
    
    def get_plans(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Récupère tous les plans"""
        return self.db.get_plans(limit)
    
    def get_plan_by_id(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un plan par son ID"""
        plans = self.db.get_plans(1000)
        for plan in plans:
            if plan['id'] == plan_id:
                return plan
        return None
    
    def delete_plan(self, plan_id: int) -> bool:
        """Supprime un plan et tous ses repas"""
        return self.db.delete_plan(plan_id)
    
    def generate_ai_plan(self, preferences: UserPreferences, 
                        plan_name: str, week_start_date: date) -> Dict[str, Any]:
        """Génère un plan avec l'IA en utilisant Gemini AI"""
        try:
            # Importer les services nécessaires (lazy import pour éviter les cycles)
            from services.meal_service import MealService
            from services.ai_service import AIService
            from services.hybrid_recipe_service import HybridRecipeService
            
            meal_service = MealService(self.db)
            ai_service = AIService()
            hybrid_service = HybridRecipeService(self.db)
            
            # 1. Créer le plan vide
            plan_id = self.create_plan(plan_name, week_start_date, preferences)
            
            # 2. Générer les recettes avec le service hybride
            weekly_recipes = hybrid_service.generate_weekly_plan_recipes(preferences, plan_id)
            
            # 3. Ajouter les repas générés
            added_count = 0
            for meal_data in weekly_recipes:
                try:
                    meal_service.add_meal(meal_data)
                    added_count += 1
                except Exception as e:
                    print(f"Erreur ajout repas {meal_data.get('recipe_name')}: {e}")
            
            # 4. Calculer les statistiques finales
            final_stats = self.get_plan_statistics(plan_id)
            quality_score = hybrid_service.get_planning_quality_score(plan_id)
            
            return {
                'success': True,
                'plan_id': plan_id,
                'meals_added': added_count,
                'total_estimated_cost': self.calculate_budget_estimate(plan_id),
                'ai_model': 'gemini-2.0-flash',
                'statistics': final_stats,
                'quality_score': quality_score,
                'dietary_notes': f"Planning généré avec {added_count} repas variés"
            }
            
        except Exception as e:
            # En cas d'erreur, retourner le plan vide quand même
            return {
                'success': False,
                'plan_id': None,
                'error': f"Erreur génération IA: {str(e)}",
                'ai_model': 'gemini-2.5-flash'
            }

    def calculate_budget_estimate(self, plan_id: int) -> float:
        """Calcule une estimation du budget pour un plan"""
        meals = self.db.get_plan_meals(plan_id)
        
        budget_per_meal = {
            'cameroun': 8.0,
            'asiatique': 6.0,
            'mexican': 7.0,
            'french': 10.0
        }
        
        total = 0.0
        for meal in meals:
            cuisine = meal.get('cuisine_type', 'cameroun')
            total += budget_per_meal.get(cuisine, 8.0)
        
        return round(total, 2)
    
    def get_plan_statistics(self, plan_id: int) -> Dict[str, Any]:
        """Récupère les statistiques d'un plan"""
        meals = self.db.get_plan_meals(plan_id)
        
        if not meals:
            return {
                'total_meals': 0,
                'avg_rating': 0,
                'favorite_count': 0,
                'cuisine_distribution': {},
                'budget_estimate': 0
            }
        
        total_meals = len(meals)
        ratings = [meal['rating'] for meal in meals if meal['rating'] > 0]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        favorite_count = sum(1 for meal in meals if meal['is_favorite'])
        
        cuisine_dist = {}
        for meal in meals:
            cuisine = meal.get('cuisine_type', 'unknown')
            cuisine_dist[cuisine] = cuisine_dist.get(cuisine, 0) + 1
        
        budget_estimate = self.calculate_budget_estimate(plan_id)
        
        return {
            'total_meals': total_meals,
            'avg_rating': round(avg_rating, 1),
            'favorite_count': favorite_count,
            'cuisine_distribution': cuisine_dist,
            'budget_estimate': budget_estimate
        }

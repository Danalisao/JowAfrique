"""
Service de gestion des plans hebdomadaires
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from models import WeeklyPlan, UserPreferences, CuisineType, BudgetLevel
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
            generated_by_ai=True,
            created_at=datetime.now()
        )
        return self.db.create_plan(plan)
    
    def get_plans(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Récupère tous les plans"""
        return self.db.get_plans(limit)
    
    def get_plan_by_id(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un plan par son ID"""
        plans = self.db.get_plans(1000)  # Récupère plus pour trouver le bon
        for plan in plans:
            if plan['id'] == plan_id:
                return plan
        return None
    
    def delete_plan(self, plan_id: int) -> bool:
        """Supprime un plan"""
        return self.db.delete_plan(plan_id)
    
    def generate_ai_plan(self, preferences: UserPreferences, 
                        plan_name: str, week_start_date: date) -> Dict[str, Any]:
        """Génère un plan avec l'IA en utilisant Gemini AI 2.5 Flash"""
        try:
            from planner_module import IntelligentPlanner
            
            # Initialiser le planificateur intelligent
            planner = IntelligentPlanner(self.db)
            
            # Générer le planning complet
            result = planner.generate_weekly_plan(preferences, plan_name, week_start_date)
            
            if result['success']:
                return {
                    'id': result['plan_id'],
                    'plan_name': plan_name,
                    'week_start_date': week_start_date.isoformat(),
                    'meals': [],  # Les repas sont ajoutés directement
                    'total_recipes': result['meals_added'],
                    'generated_by_ai': True,
                    'ai_model': result.get('ai_model', 'gemini-2.0-flash-exp'),
                    'total_estimated_cost': result.get('total_estimated_cost', 0),
                    'statistics': result.get('statistics', {}),
                    'dietary_notes': result.get('dietary_notes', '')
                }
            else:
                # Fallback : créer un plan vide en cas d'erreur IA
                plan_id = self.create_plan(plan_name, week_start_date, preferences)
                return {
                    'id': plan_id,
                    'plan_name': plan_name,
                    'week_start_date': week_start_date.isoformat(),
                    'meals': [],
                    'total_recipes': 0,
                    'generated_by_ai': True,
                    'ai_error': result.get('error', 'Erreur inconnue')
                }
                
        except Exception as e:
            # Fallback en cas d'erreur d'import ou d'initialisation
            plan_id = self.create_plan(plan_name, week_start_date, preferences)
            return {
                'id': plan_id,
                'plan_name': plan_name,
                'week_start_date': week_start_date.isoformat(),
                'meals': [],
                'total_recipes': 0,
                'generated_by_ai': True,
                'ai_error': f"Erreur initialisation IA: {str(e)}"
            }
    
    def calculate_budget_estimate(self, plan_id: int) -> float:
        """Calcule une estimation du budget pour un plan"""
        meals = self.db.get_plan_meals(plan_id)
        
        # Estimation basique basée sur le type de cuisine
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
        
        # Calculs des statistiques
        total_meals = len(meals)
        ratings = [meal['rating'] for meal in meals if meal['rating'] > 0]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        favorite_count = sum(1 for meal in meals if meal['is_favorite'])
        
        # Distribution des cuisines
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

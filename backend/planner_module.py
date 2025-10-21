"""
Module de planification intelligente avec Gemini AI
"""
from typing import List, Dict, Any, Optional
from datetime import date, timedelta
from services.ai_service import AIService
from services.meal_service import MealService
from services.plan_service import PlanService
from services.hybrid_recipe_service import HybridRecipeService
from services.constraint_service import ConstraintService
from models import UserPreferences, CuisineType, BudgetLevel, MealType
from database import DatabaseManager

class IntelligentPlanner:
    def __init__(self, db_manager: DatabaseManager):
        """Initialise le planificateur intelligent"""
        self.db = db_manager
        self.ai_service = AIService()
        self.meal_service = MealService(db_manager)
        self.plan_service = PlanService(db_manager)
        self.hybrid_service = HybridRecipeService(db_manager)
        self.constraint_service = ConstraintService(db_manager)
    
    def generate_weekly_plan(self, preferences: UserPreferences, 
                           plan_name: str, week_start_date: date) -> Dict[str, Any]:
        """Génère un planning hebdomadaire complet avec IA et contraintes"""
        
        try:
            # 1. Créer le plan dans la base de données d'abord
            plan_id = self.plan_service.create_plan(
                plan_name=plan_name,
                week_start_date=week_start_date,
                preferences=preferences
            )
            
            # 2. Générer les recettes avec le service hybride
            weekly_recipes = self.hybrid_service.generate_weekly_plan_recipes(
                preferences, plan_id
            )
            
            # 3. Ajouter les repas générés
            added_meals = []
            for meal_data in weekly_recipes:
                try:
                    meal_id = self._add_ai_generated_meal(plan_id, meal_data)
                    added_meals.append(meal_id)
                except Exception as e:
                    print(f"Erreur ajout repas {meal_data['recipe_name']}: {e}")
            
            # 4. Vérifier les contraintes et ajuster si nécessaire
            self._adjust_plan_constraints(plan_id, preferences)
            
            # 5. Calculer les statistiques finales
            final_stats = self._calculate_plan_statistics(plan_id)
            quality_score = self.hybrid_service.get_planning_quality_score(plan_id)
            
            return {
                'success': True,
                'plan_id': plan_id,
                'meals_added': len(added_meals),
                'total_estimated_cost': self._calculate_total_cost(plan_id),
                'ai_model': 'gemini-2.0-flash-exp',
                'statistics': final_stats,
                'quality_score': quality_score,
                'dietary_notes': f"Planning généré avec {len(added_meals)} dîners variés"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Erreur génération planning: {str(e)}",
                'ai_model': 'gemini-2.0-flash-exp'
            }
    
    def _add_ai_generated_meal(self, plan_id: int, meal_data: Dict[str, Any]) -> int:
        """Ajoute un repas généré par l'IA à un plan"""
        
        # Convertir les données de l'IA vers le format de la base
        meal_dict = {
            'day_of_week': meal_data['day_of_week'],
            'meal_type': meal_data['meal_type'],
            'recipe_name': meal_data['recipe_name'],
            'main_ingredient': meal_data.get('main_ingredient', ''),
            'cuisine_type': meal_data.get('cuisine_type', 'cameroun'),
            'prep_time': meal_data.get('prep_time', 30),
            'cook_time': meal_data.get('cook_time', 45),
            'notes': meal_data.get('notes', ''),
            'plan_id': plan_id,
            'is_favorite': False,
            'rating': 0
        }
        
        return self.meal_service.add_meal(meal_dict)
    
    def _calculate_plan_statistics(self, plan_id: int) -> Dict[str, Any]:
        """Calcule les statistiques d'un plan"""
        meals = self.meal_service.get_meals_by_plan(plan_id)
        
        if not meals:
            return {}
        
        # Statistiques de base
        total_meals = len(meals)
        cuisines = {}
        ingredients = {}
        total_prep_time = 0
        total_cook_time = 0
        
        for meal in meals:
            # Comptage des cuisines
            cuisine = meal.get('cuisine_type', 'cameroun')
            cuisines[cuisine] = cuisines.get(cuisine, 0) + 1
            
            # Comptage des ingrédients
            ingredient = meal.get('main_ingredient', '')
            if ingredient:
                ingredients[ingredient] = ingredients.get(ingredient, 0) + 1
            
            # Temps de préparation
            total_prep_time += meal.get('prep_time', 0)
            total_cook_time += meal.get('cook_time', 0)
        
        return {
            'total_meals': total_meals,
            'cuisine_distribution': cuisines,
            'top_ingredients': sorted(ingredients.items(), key=lambda x: x[1], reverse=True)[:5],
            'avg_prep_time': round(total_prep_time / total_meals, 1) if total_meals > 0 else 0,
            'avg_cook_time': round(total_cook_time / total_meals, 1) if total_meals > 0 else 0,
            'total_cooking_time': total_prep_time + total_cook_time
        }
    
    def suggest_meal_variations(self, meal_id: int, preferences: UserPreferences) -> List[Dict[str, Any]]:
        """Suggère des variations d'un repas existant"""
        
        # Récupérer le repas
        meals = self.meal_service.get_meals_by_plan(None)  # Récupérer tous les repas
        meal = next((m for m in meals if m['id'] == meal_id), None)
        
        if not meal:
            return []
        
        # Générer des variations avec l'IA
        variations = self.ai_service.suggest_meal_variations(meal, preferences)
        
        return variations
    
    def optimize_shopping_list(self, plan_id: int, budget: float) -> Dict[str, Any]:
        """Optimise la liste de courses d'un plan"""
        
        # Générer la liste de courses de base
        shopping_list = self.meal_service.generate_shopping_list(plan_id)
        
        # Optimiser avec l'IA
        optimization = self.ai_service.generate_shopping_optimization(shopping_list, budget)
        
        return optimization
    
    def analyze_nutritional_balance(self, plan_id: int) -> Dict[str, Any]:
        """Analyse l'équilibre nutritionnel d'un plan"""
        
        meals = self.meal_service.get_meals_by_plan(plan_id)
        
        if not meals:
            return {'error': 'Aucun repas trouvé dans ce plan'}
        
        # Analyser avec l'IA
        analysis = self.ai_service.analyze_nutritional_balance(meals)
        
        return analysis
    
    def regenerate_plan_day(self, plan_id: int, day_of_week: str, 
                          preferences: UserPreferences) -> Dict[str, Any]:
        """Régénère les repas d'un jour spécifique"""
        
        try:
            # Supprimer les repas existants du jour
            meals = self.meal_service.get_meals_by_plan(plan_id)
            for meal in meals:
                if meal['day_of_week'] == day_of_week:
                    self.meal_service.remove_meal(meal['id'])
            
            # Générer de nouveaux repas pour ce jour
            day_preferences = UserPreferences(
                cuisines=preferences.cuisines,
                budget=preferences.budget,
                light=preferences.light,
                vegetarian=preferences.vegetarian
            )
            
            # Créer un mini-plan pour ce jour
            temp_plan_name = f"Régénération {day_of_week}"
            temp_date = date.today()  # Date temporaire
            
            ai_result = self.ai_service.generate_weekly_plan(
                day_preferences, temp_plan_name, temp_date
            )
            
            if not ai_result['success']:
                return ai_result
            
            # Filtrer les repas du jour demandé
            day_meals = [meal for meal in ai_result['data']['meals'] 
                        if meal['day_of_week'] == day_of_week]
            
            # Ajouter les nouveaux repas
            added_meals = []
            for meal_data in day_meals:
                meal_id = self._add_ai_generated_meal(plan_id, meal_data)
                added_meals.append(meal_id)
            
            return {
                'success': True,
                'day_of_week': day_of_week,
                'meals_added': len(added_meals),
                'ai_model': ai_result['ai_model']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Erreur régénération jour: {str(e)}"
            }
    
    def get_ai_recommendations(self, user_history: List[Dict[str, Any]], 
                             preferences: UserPreferences) -> Dict[str, Any]:
        """Génère des recommandations personnalisées basées sur l'historique"""
        
        # Analyser l'historique utilisateur
        history_text = self._format_user_history(user_history)
        
        prompt = f"""
Basé sur l'historique de cet utilisateur :

{history_text}

Préférences actuelles :
- Cuisines : {', '.join([c.value for c in preferences.cuisines])}
- Budget : {preferences.budget.value}
- Léger : {'Oui' if preferences.light else 'Non'}
- Végétarien : {'Oui' if preferences.vegetarian else 'Non'}

Génère des recommandations personnalisées :

Format JSON :
{{
  "recommendations": [
    {{
      "type": "recipe",
      "title": "Titre de la recommandation",
      "description": "Description détaillée",
      "reason": "Pourquoi cette recommandation",
      "priority": "high|medium|low"
    }}
  ],
  "insights": [
    "Insight 1 sur les habitudes",
    "Insight 2 sur les préférences"
  ],
  "suggested_improvements": [
    "Amélioration 1",
    "Amélioration 2"
  ]
}}
"""
        
        try:
            response = self.ai_service.model.generate_content(prompt)
            recommendations = self.ai_service._parse_ai_response(response.text)
            return recommendations
        except Exception as e:
            return {
                'recommendations': [],
                'insights': [],
                'suggested_improvements': []
            }
    
    def _format_user_history(self, history: List[Dict[str, Any]]) -> str:
        """Formate l'historique utilisateur pour l'IA"""
        
        if not history:
            return "Aucun historique disponible"
        
        formatted = []
        for item in history:
            if 'recipe_name' in item:
                formatted.append(f"- {item['recipe_name']} ({item.get('cuisine_type', 'cameroun')}) - Note: {item.get('rating', 'N/A')}")
        
        return "\n".join(formatted[:20])  # Limiter à 20 entrées
    
    def _adjust_plan_constraints(self, plan_id: int, preferences: UserPreferences):
        """Ajuste le planning pour respecter les contraintes"""
        
        # Vérifier les violations de contraintes
        stats = self.constraint_service.get_planning_statistics(plan_id)
        violations = stats.get('constraint_violations', [])
        
        if violations:
            print(f"Violations détectées: {violations}")
            # Ici on pourrait implémenter une logique de correction automatique
            # Pour l'instant, on log juste les violations
    
    def _calculate_total_cost(self, plan_id: int) -> float:
        """Calcule le coût total estimé d'un planning"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT SUM(prep_time * 0.5 + cook_time * 0.3) as total_cost
                    FROM meal_slots
                    WHERE plan_id = ?
                """, (plan_id,))
                
                result = cursor.fetchone()
                return result[0] if result[0] else 0.0
                
        except Exception as e:
            print(f"Erreur calcul coût: {e}")
            return 0.0

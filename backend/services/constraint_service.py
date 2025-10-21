"""
Service de gestion des contraintes de planification
"""
from typing import List, Dict, Any, Optional, Set
from datetime import date, timedelta
from database import DatabaseManager
from models import CuisineType, MealType

class ConstraintService:
    def __init__(self, db_manager: DatabaseManager):
        """Initialise le service de contraintes"""
        self.db = db_manager
    
    def get_previous_plans(self, weeks_back: int = 4) -> List[Dict[str, Any]]:
        """Récupère les plannings des semaines précédentes"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Calculer la date de début (4 semaines en arrière)
                start_date = date.today() - timedelta(weeks=weeks_back)
                
                cursor.execute("""
                    SELECT wp.id, wp.plan_name, wp.week_start_date
                    FROM weekly_plans wp
                    WHERE wp.week_start_date >= ?
                    ORDER BY wp.week_start_date DESC
                """, (start_date,))
                
                plans = []
                for row in cursor.fetchall():
                    plans.append({
                        'id': row[0],
                        'plan_name': row[1],
                        'week_start_date': row[2]
                    })
                
                return plans
                
        except Exception as e:
            print(f"Erreur récupération plannings précédents: {e}")
            return []
    
    def get_used_recipes(self, weeks_back: int = 4) -> Set[str]:
        """Récupère les recettes utilisées dans les plannings précédents"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Calculer la date de début
                start_date = date.today() - timedelta(weeks=weeks_back)
                
                cursor.execute("""
                    SELECT DISTINCT ms.recipe_name
                    FROM meal_slots ms
                    JOIN weekly_plans wp ON ms.plan_id = wp.id
                    WHERE wp.week_start_date >= ?
                """, (start_date,))
                
                used_recipes = set()
                for row in cursor.fetchall():
                    used_recipes.add(row[0])
                
                return used_recipes
                
        except Exception as e:
            print(f"Erreur récupération recettes utilisées: {e}")
            return set()
    
    def get_used_ingredients_by_week(self, plan_id: int) -> Dict[str, int]:
        """Récupère les ingrédients utilisés dans un planning avec leur fréquence"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT main_ingredient, COUNT(*) as count
                    FROM meal_slots
                    WHERE plan_id = ?
                    GROUP BY main_ingredient
                """, (plan_id,))
                
                ingredients = {}
                for row in cursor.fetchall():
                    ingredients[row[0]] = row[1]
                
                return ingredients
                
        except Exception as e:
            print(f"Erreur récupération ingrédients: {e}")
            return {}
    
    def get_consecutive_ingredients(self, plan_id: int) -> List[tuple]:
        """Récupère les ingrédients consécutifs dans un planning"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT day_of_week, main_ingredient
                    FROM meal_slots
                    WHERE plan_id = ?
                    ORDER BY 
                        CASE day_of_week
                            WHEN 'Lundi' THEN 1
                            WHEN 'Mardi' THEN 2
                            WHEN 'Mercredi' THEN 3
                            WHEN 'Jeudi' THEN 4
                            WHEN 'Vendredi' THEN 5
                            WHEN 'Samedi' THEN 6
                            WHEN 'Dimanche' THEN 7
                        END
                """, (plan_id,))
                
                meals = cursor.fetchall()
                consecutive = []
                
                for i in range(len(meals) - 1):
                    if meals[i][1] == meals[i + 1][1]:
                        consecutive.append((meals[i][0], meals[i + 1][0], meals[i][1]))
                
                return consecutive
                
        except Exception as e:
            print(f"Erreur récupération ingrédients consécutifs: {e}")
            return []
    
    def check_recipe_constraints(self, recipe_name: str, used_recipes: Set[str]) -> bool:
        """Vérifie si une recette respecte les contraintes de répétition"""
        # Même recette ne doit pas revenir dans les 2 semaines précédentes
        return recipe_name not in used_recipes
    
    def check_ingredient_constraints(self, ingredient: str, current_plan_ingredients: Dict[str, int], 
                                   consecutive_ingredients: List[tuple]) -> bool:
        """Vérifie si un ingrédient respecte les contraintes"""
        
        # Ingrédients comme riz, pâtes ne doivent pas apparaître plus d'une fois
        restricted_ingredients = {'riz', 'pâtes', 'pates', 'pasta', 'rice'}
        if ingredient.lower() in restricted_ingredients:
            return current_plan_ingredients.get(ingredient, 0) == 0
        
        return True
    
    def check_consecutive_constraints(self, ingredient: str, day_of_week: str, 
                                    current_plan_ingredients: Dict[str, int]) -> bool:
        """Vérifie les contraintes d'ingrédients consécutifs"""
        
        # Ingrédients comme riz, pâtes ne doivent pas se suivre
        restricted_ingredients = {'riz', 'pâtes', 'pates', 'pasta', 'rice'}
        if ingredient.lower() not in restricted_ingredients:
            return True
        
        # Vérifier le jour précédent
        previous_day = self._get_previous_day(day_of_week)
        if previous_day and current_plan_ingredients.get(previous_day) == ingredient:
            return False
        
        return True
    
    def _get_previous_day(self, day_of_week: str) -> Optional[str]:
        """Retourne le jour précédent"""
        days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        try:
            index = days.index(day_of_week)
            return days[index - 1] if index > 0 else None
        except ValueError:
            return None
    
    def filter_recipes_by_constraints(self, recipes: List[Dict[str, Any]], 
                                    used_recipes: Set[str],
                                    current_plan_ingredients: Dict[str, int],
                                    day_of_week: str) -> List[Dict[str, Any]]:
        """Filtre les recettes selon les contraintes"""
        
        filtered_recipes = []
        
        for recipe in recipes:
            recipe_name = recipe.get('recipe_name', '')
            main_ingredient = recipe.get('main_ingredient', '')
            
            # Vérifier les contraintes
            if not self.check_recipe_constraints(recipe_name, used_recipes):
                continue
            
            if not self.check_ingredient_constraints(main_ingredient, current_plan_ingredients, []):
                continue
            
            if not self.check_consecutive_constraints(main_ingredient, day_of_week, current_plan_ingredients):
                continue
            
            filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    def get_planning_statistics(self, plan_id: int) -> Dict[str, Any]:
        """Génère des statistiques sur un planning"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Statistiques générales
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_meals,
                        COUNT(DISTINCT main_ingredient) as unique_ingredients,
                        COUNT(DISTINCT cuisine_type) as unique_cuisines
                    FROM meal_slots
                    WHERE plan_id = ?
                """, (plan_id,))
                
                stats = cursor.fetchone()
                
                # Ingrédients les plus utilisés
                cursor.execute("""
                    SELECT main_ingredient, COUNT(*) as count
                    FROM meal_slots
                    WHERE plan_id = ?
                    GROUP BY main_ingredient
                    ORDER BY count DESC
                """, (plan_id,))
                
                top_ingredients = cursor.fetchall()
                
                # Cuisines
                cursor.execute("""
                    SELECT cuisine_type, COUNT(*) as count
                    FROM meal_slots
                    WHERE plan_id = ?
                    GROUP BY cuisine_type
                    ORDER BY count DESC
                """, (plan_id,))
                
                cuisines = cursor.fetchall()
                
                return {
                    'total_meals': stats[0],
                    'unique_ingredients': stats[1],
                    'unique_cuisines': stats[2],
                    'top_ingredients': top_ingredients,
                    'cuisines': cuisines,
                    'constraint_violations': self._check_constraint_violations(plan_id)
                }
                
        except Exception as e:
            print(f"Erreur statistiques planning: {e}")
            return {}
    
    def _check_constraint_violations(self, plan_id: int) -> List[str]:
        """Vérifie les violations de contraintes dans un planning"""
        violations = []
        
        # Vérifier les ingrédients consécutifs
        consecutive = self.get_consecutive_ingredients(plan_id)
        for day1, day2, ingredient in consecutive:
            violations.append(f"Ingrédient '{ingredient}' consécutif: {day1} -> {day2}")
        
        # Vérifier les ingrédients répétés
        ingredients = self.get_used_ingredients_by_week(plan_id)
        for ingredient, count in ingredients.items():
            if count > 1:
                violations.append(f"Ingrédient '{ingredient}' utilisé {count} fois")
        
        return violations

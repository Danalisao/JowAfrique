"""
Service hybride combinant recettes Jow et recettes camerounaises
"""
from typing import List, Dict, Any, Optional, Set
from database import DatabaseManager
from services.jow_service import JowService
from services.constraint_service import ConstraintService
from models import CuisineType, MealType, UserPreferences

class HybridRecipeService:
    def __init__(self, db_manager: DatabaseManager):
        """Initialise le service hybride"""
        self.db = db_manager
        self.jow_service = JowService()
        self.constraint_service = ConstraintService(db_manager)
    
    def get_available_recipes(self, preferences: UserPreferences, 
                            day_of_week: str,
                            current_plan_ingredients: Dict[str, int] = None) -> List[Dict[str, Any]]:
        """Récupère les recettes disponibles en respectant les contraintes"""
        
        if current_plan_ingredients is None:
            current_plan_ingredients = {}
        
        # 1. Récupérer les recettes camerounaises
        cameroon_recipes = self._get_cameroon_recipes()
        
        # 2. Récupérer les recettes Jow
        jow_recipes = self._get_jow_recipes(preferences)
        
        # 3. Combiner les recettes
        all_recipes = cameroon_recipes + jow_recipes
        
        # 4. Appliquer les contraintes
        used_recipes = self.constraint_service.get_used_recipes()
        filtered_recipes = self.constraint_service.filter_recipes_by_constraints(
            all_recipes, used_recipes, current_plan_ingredients, day_of_week
        )
        
        # 5. S'assurer qu'il y a toujours au moins une recette camerounaise
        cameroon_filtered = [r for r in filtered_recipes if r.get('cuisine_type') == 'cameroun']
        if not cameroon_filtered:
            # Ajouter des recettes camerounaises même si elles violent les contraintes
            cameroon_available = [r for r in cameroon_recipes if r.get('recipe_name') not in used_recipes]
            if cameroon_available:
                filtered_recipes.extend(cameroon_available[:2])  # Ajouter 2 recettes camerounaises
        
        return filtered_recipes
    
    def _get_cameroon_recipes(self) -> List[Dict[str, Any]]:
        """Récupère les recettes camerounaises de la base"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        id, recipe_name, main_ingredient, cuisine_type,
                        image_url, prep_time, cook_time, notes,
                        is_favorite, rating, jow_recipe_id, jow_recipe_url
                    FROM meal_slots
                    WHERE cuisine_type = ? AND plan_id IS NULL
                    ORDER BY rating DESC, is_favorite DESC
                """, (CuisineType.CAMEROUN.value,))
                
                recipes = []
                for row in cursor.fetchall():
                    recipes.append({
                        'id': row[0],
                        'recipe_name': row[1],
                        'main_ingredient': row[2],
                        'cuisine_type': row[3],
                        'image_url': row[4],
                        'prep_time': row[5],
                        'cook_time': row[6],
                        'notes': row[7],
                        'is_favorite': bool(row[8]),
                        'rating': row[9],
                        'jow_recipe_id': row[10],
                        'jow_recipe_url': row[11],
                        'source': 'local'
                    })
                
                return recipes
                
        except Exception as e:
            print(f"Erreur récupération recettes camerounaises: {e}")
            return []
    
    def _get_jow_recipes(self, preferences: UserPreferences) -> List[Dict[str, Any]]:
        """Récupère les recettes Jow selon les préférences"""
        try:
            # Construire les préférences pour Jow
            jow_preferences = {
                'cuisines': [c.value for c in preferences.cuisines if c != CuisineType.CAMEROUN],
                'vegetarian': preferences.vegetarian,
                'light': preferences.light
            }
            
            # Récupérer les suggestions Jow
            jow_recipes = self.jow_service.get_recipe_suggestions(jow_preferences)
            
            # Limiter le nombre de recettes Jow
            return jow_recipes[:10]  # Maximum 10 recettes Jow
            
        except Exception as e:
            print(f"Erreur récupération recettes Jow: {e}")
            return []
    
    def generate_weekly_plan_recipes(self, preferences: UserPreferences, 
                                   plan_id: int) -> List[Dict[str, Any]]:
        """Génère les recettes pour un planning hebdomadaire"""
        
        days_of_week = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        weekly_recipes = []
        current_plan_ingredients = {}
        
        for day in days_of_week:
            # Récupérer les recettes disponibles pour ce jour
            available_recipes = self.get_available_recipes(
                preferences, day, current_plan_ingredients
            )
            
            if not available_recipes:
                # Fallback: utiliser n'importe quelle recette camerounaise
                available_recipes = self._get_cameroon_recipes()[:5]
            
            # Sélectionner une recette (priorité aux camerounaises)
            selected_recipe = self._select_recipe_for_day(available_recipes, day)
            
            if selected_recipe:
                # Ajouter les informations du jour
                selected_recipe['day_of_week'] = day
                selected_recipe['meal_type'] = MealType.DINNER.value
                selected_recipe['plan_id'] = plan_id
                
                weekly_recipes.append(selected_recipe)
                
                # Mettre à jour les ingrédients utilisés
                ingredient = selected_recipe.get('main_ingredient', '')
                if ingredient:
                    current_plan_ingredients[ingredient] = current_plan_ingredients.get(ingredient, 0) + 1
        
        return weekly_recipes
    
    def _select_recipe_for_day(self, available_recipes: List[Dict[str, Any]], 
                              day_of_week: str) -> Optional[Dict[str, Any]]:
        """Sélectionne une recette pour un jour donné"""
        
        if not available_recipes:
            return None
        
        # Priorité aux recettes camerounaises
        cameroon_recipes = [r for r in available_recipes if r.get('cuisine_type') == 'cameroun']
        if cameroon_recipes:
            # Sélectionner la meilleure recette camerounaise
            return max(cameroon_recipes, key=lambda x: (x.get('rating', 0), x.get('is_favorite', False)))
        
        # Sinon, sélectionner la meilleure recette disponible
        return max(available_recipes, key=lambda x: (x.get('rating', 0), x.get('is_favorite', False)))
    
    def get_recipe_variations(self, base_recipe: Dict[str, Any], 
                            preferences: UserPreferences) -> List[Dict[str, Any]]:
        """Génère des variations d'une recette"""
        
        # Si c'est une recette camerounaise, chercher des variations locales
        if base_recipe.get('cuisine_type') == 'cameroun':
            return self._get_cameroon_variations(base_recipe)
        
        # Sinon, chercher des variations Jow
        return self._get_jow_variations(base_recipe, preferences)
    
    def _get_cameroon_variations(self, base_recipe: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Génère des variations de recettes camerounaises"""
        
        main_ingredient = base_recipe.get('main_ingredient', '')
        variations = []
        
        # Chercher des recettes avec le même ingrédient principal
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        id, recipe_name, main_ingredient, cuisine_type,
                        image_url, prep_time, cook_time, notes,
                        is_favorite, rating
                    FROM meal_slots
                    WHERE main_ingredient = ? 
                    AND cuisine_type = ?
                    AND id != ?
                    AND plan_id IS NULL
                    ORDER BY rating DESC
                    LIMIT 3
                """, (main_ingredient, CuisineType.CAMEROUN.value, base_recipe.get('id', 0)))
                
                for row in cursor.fetchall():
                    variations.append({
                        'id': row[0],
                        'recipe_name': row[1],
                        'main_ingredient': row[2],
                        'cuisine_type': row[3],
                        'image_url': row[4],
                        'prep_time': row[5],
                        'cook_time': row[6],
                        'notes': row[7],
                        'is_favorite': bool(row[8]),
                        'rating': row[9],
                        'source': 'local'
                    })
                
        except Exception as e:
            print(f"Erreur récupération variations camerounaises: {e}")
        
        return variations
    
    def _get_jow_variations(self, base_recipe: Dict[str, Any], 
                          preferences: UserPreferences) -> List[Dict[str, Any]]:
        """Génère des variations de recettes Jow"""
        
        # Rechercher des recettes similaires sur Jow
        main_ingredient = base_recipe.get('main_ingredient', '')
        cuisine = base_recipe.get('cuisine_type', '')
        
        # Construire la requête de recherche
        search_query = f"{main_ingredient} {cuisine}"
        
        try:
            jow_recipes = self.jow_service.search_recipes(search_query, limit=5)
            return jow_recipes
        except Exception as e:
            print(f"Erreur récupération variations Jow: {e}")
            return []
    
    def get_planning_quality_score(self, plan_id: int) -> Dict[str, Any]:
        """Calcule un score de qualité pour un planning"""
        
        stats = self.constraint_service.get_planning_statistics(plan_id)
        
        # Score de base
        score = 100
        
        # Pénalités pour violations
        violations = stats.get('constraint_violations', [])
        score -= len(violations) * 10
        
        # Bonus pour diversité
        unique_ingredients = stats.get('unique_ingredients', 0)
        if unique_ingredients >= 5:
            score += 10
        elif unique_ingredients >= 3:
            score += 5
        
        # Bonus pour recettes camerounaises
        cameroon_count = sum(1 for c in stats.get('cuisines', []) if c[0] == 'cameroun')
        if cameroon_count >= 3:
            score += 15
        elif cameroon_count >= 1:
            score += 10
        
        return {
            'score': max(0, min(100, score)),
            'violations': violations,
            'stats': stats,
            'recommendations': self._get_improvement_recommendations(stats)
        }
    
    def _get_improvement_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Génère des recommandations d'amélioration"""
        
        recommendations = []
        
        # Vérifier la diversité des ingrédients
        unique_ingredients = stats.get('unique_ingredients', 0)
        if unique_ingredients < 5:
            recommendations.append("Ajouter plus de diversité dans les ingrédients")
        
        # Vérifier les recettes camerounaises
        cameroon_count = sum(1 for c in stats.get('cuisines', []) if c[0] == 'cameroun')
        if cameroon_count == 0:
            recommendations.append("Inclure au moins une recette camerounaise")
        
        # Vérifier les violations
        violations = stats.get('constraint_violations', [])
        if violations:
            recommendations.append("Réduire les répétitions d'ingrédients")
        
        return recommendations

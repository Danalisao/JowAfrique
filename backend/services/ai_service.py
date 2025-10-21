"""
Service d'intégration avec Gemini AI 2.5 Flash
"""
import os
import json
from typing import List, Dict, Any, Optional
from datetime import date, timedelta
import google.generativeai as genai
from dotenv import load_dotenv
from models import UserPreferences, CuisineType, BudgetLevel, MealType

# Charger les variables d'environnement
load_dotenv()

class AIService:
    def __init__(self):
        """Initialise le service Gemini AI"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY non trouvée dans les variables d'environnement")
        
        # Configuration de Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def generate_weekly_plan(self, preferences: UserPreferences, 
                           plan_name: str, week_start_date: date,
                           hybrid_service=None) -> Dict[str, Any]:
        """Génère un planning hebdomadaire avec Gemini AI et service hybride"""
        
        # Construire le prompt pour Gemini
        prompt = self._build_planning_prompt(preferences, plan_name, week_start_date)
        
        try:
            # Appel à Gemini AI
            response = self.model.generate_content(prompt)
            
            # Parser la réponse JSON
            plan_data = self._parse_ai_response(response.text)
            
            # Si on a un service hybride, enrichir avec les vraies recettes
            if hybrid_service:
                plan_data = self._enrich_with_hybrid_recipes(plan_data, hybrid_service, preferences)
            
            return {
                'success': True,
                'data': plan_data,
                'ai_model': 'gemini-2.0-flash-exp'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Erreur Gemini AI: {str(e)}",
                'ai_model': 'gemini-2.0-flash-exp'
            }
    
    def _build_planning_prompt(self, preferences: UserPreferences, 
                              plan_name: str, week_start_date: date) -> str:
        """Construit le prompt pour Gemini AI"""
        
        # Convertir les préférences en texte
        cuisines_text = ", ".join([c.value for c in preferences.cuisines])
        budget_text = preferences.budget.value
        
        # Calculer les dates de la semaine
        week_dates = [week_start_date + timedelta(days=i) for i in range(7)]
        days_of_week = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        
        prompt = f"""
Tu es un expert en planification de repas africains, spécialement pour le Cameroun et l'Afrique de l'Ouest.

Génère un planning de DINERS uniquement pour la semaine avec les spécifications suivantes :

**Informations du plan :**
- Nom du plan : {plan_name}
- Semaine du : {week_start_date.strftime('%d/%m/%Y')}
- Cuisines préférées : {cuisines_text}
- Budget : {budget_text}
- Léger : {'Oui' if preferences.light else 'Non'}
- Végétarien : {'Oui' if preferences.vegetarian else 'Non'}

**Contraintes :**
- UNIQUEMENT des repas du DINER (pas de déjeuner)
- Focus sur les recettes camerounaises et africaines authentiques
- Équilibrer les dîners sur la semaine
- Varier les ingrédients principaux
- Respecter le budget {budget_text}
- Inclure des plats traditionnels populaires pour le dîner

**Format de réponse attendu (JSON strict) :**
{{
  "plan_name": "{plan_name}",
  "week_start_date": "{week_start_date.isoformat()}",
  "meals": [
    {{
      "day_of_week": "Lundi",
      "meal_type": "Dîner",
      "recipe_name": "Nom de la recette",
      "main_ingredient": "Ingrédient principal",
      "cuisine_type": "cameroun",
      "prep_time": 30,
      "cook_time": 45,
      "notes": "Notes sur la recette",
      "estimated_cost": 8.0
    }}
  ],
  "total_estimated_cost": 28.0,
  "dietary_notes": "Notes sur l'équilibre nutritionnel des dîners"
}}

**Recettes camerounaises populaires pour le DINER :**
- Ndolé, Eru, Koki, Achu, Nkui
- Riz au gras, Taro aux épinards, Plantain mûr
- Poisson braisé, Poulet braisé, Kati-kati
- Soupes traditionnelles, Plats mijotés
- Salades africaines, Légumes sautés

Génère un planning équilibré et varié pour 7 dîners de la semaine (un dîner par jour).
"""
        
        return prompt
    
    def _enrich_with_hybrid_recipes(self, plan_data: Dict[str, Any], 
                                   hybrid_service, preferences: UserPreferences) -> Dict[str, Any]:
        """Enrichit le planning avec les vraies recettes du service hybride"""
        
        try:
            # Récupérer les recettes disponibles
            available_recipes = hybrid_service.get_available_recipes(preferences, "Lundi")
            
            # Créer un mapping des recettes par nom
            recipe_map = {r['recipe_name'].lower(): r for r in available_recipes}
            
            # Enrichir chaque repas avec les vraies données
            enriched_meals = []
            for meal in plan_data.get('meals', []):
                recipe_name = meal.get('recipe_name', '').lower()
                
                # Chercher une recette correspondante
                if recipe_name in recipe_map:
                    real_recipe = recipe_map[recipe_name]
                    # Mettre à jour avec les vraies données
                    meal.update({
                        'recipe_name': real_recipe['recipe_name'],
                        'main_ingredient': real_recipe['main_ingredient'],
                        'cuisine_type': real_recipe['cuisine_type'],
                        'image_url': real_recipe.get('image_url'),
                        'prep_time': real_recipe.get('prep_time', 30),
                        'cook_time': real_recipe.get('cook_time', 45),
                        'notes': real_recipe.get('notes', ''),
                        'jow_recipe_id': real_recipe.get('jow_recipe_id'),
                        'jow_recipe_url': real_recipe.get('jow_recipe_url'),
                        'source': real_recipe.get('source', 'ai')
                    })
                else:
                    # Si pas trouvé, chercher une recette similaire
                    similar_recipe = self._find_similar_recipe(meal, available_recipes)
                    if similar_recipe:
                        meal.update(similar_recipe)
                
                enriched_meals.append(meal)
            
            plan_data['meals'] = enriched_meals
            return plan_data
            
        except Exception as e:
            print(f"Erreur enrichissement recettes: {e}")
            return plan_data
    
    def _find_similar_recipe(self, meal: Dict[str, Any], available_recipes: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Trouve une recette similaire"""
        
        meal_ingredient = meal.get('main_ingredient', '').lower()
        meal_cuisine = meal.get('cuisine_type', '').lower()
        
        # Chercher par ingrédient principal
        for recipe in available_recipes:
            if (recipe.get('main_ingredient', '').lower() == meal_ingredient or
                recipe.get('cuisine_type', '').lower() == meal_cuisine):
                return {
                    'recipe_name': recipe['recipe_name'],
                    'main_ingredient': recipe['main_ingredient'],
                    'cuisine_type': recipe['cuisine_type'],
                    'image_url': recipe.get('image_url'),
                    'prep_time': recipe.get('prep_time', 30),
                    'cook_time': recipe.get('cook_time', 45),
                    'notes': recipe.get('notes', ''),
                    'jow_recipe_id': recipe.get('jow_recipe_id'),
                    'jow_recipe_url': recipe.get('jow_recipe_url'),
                    'source': recipe.get('source', 'ai')
                }
        
        return None
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse la réponse JSON de Gemini AI"""
        try:
            # Nettoyer la réponse (enlever markdown si présent)
            cleaned_response = response_text.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            # Parser le JSON
            plan_data = json.loads(cleaned_response)
            
            # Valider la structure
            if 'meals' not in plan_data:
                raise ValueError("Structure de réponse invalide : 'meals' manquant")
            
            return plan_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de parsing JSON: {str(e)}")
        except Exception as e:
            raise ValueError(f"Erreur de validation: {str(e)}")
    
    def suggest_meal_variations(self, base_meal: Dict[str, Any], 
                               preferences: UserPreferences) -> List[Dict[str, Any]]:
        """Suggère des variations d'un repas"""
        
        prompt = f"""
Basé sur ce repas : {base_meal['recipe_name']} ({base_meal['cuisine_type']})

Suggère 3 variations créatives en gardant l'esprit camerounais/africain :
- Même ingrédient principal : {base_meal['main_ingredient']}
- Cuisine préférée : {preferences.cuisines[0].value}
- Budget : {preferences.budget.value}

Format JSON :
{{
  "variations": [
    {{
      "recipe_name": "Nom de la variation",
      "main_ingredient": "Ingrédient principal",
      "cuisine_type": "cameroun",
      "prep_time": 25,
      "cook_time": 40,
      "notes": "Description de la variation"
    }}
  ]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            variations_data = self._parse_ai_response(response.text)
            return variations_data.get('variations', [])
        except Exception as e:
            print(f"Erreur génération variations: {e}")
            return []
    
    def generate_shopping_optimization(self, shopping_list: List[str], 
                                     budget: float) -> Dict[str, Any]:
        """Optimise la liste de courses avec des suggestions d'achat"""
        
        prompt = f"""
Optimise cette liste de courses pour un budget de {budget}€ :

Liste actuelle : {', '.join(shopping_list)}

Suggère :
1. Des alternatives moins chères
2. Des ingrédients de saison
3. Des quantités optimales
4. Des magasins recommandés au Cameroun

Format JSON :
{{
  "optimized_list": [
    {{
      "ingredient": "Nom de l'ingrédient",
      "quantity": "Quantité recommandée",
      "estimated_cost": 2.5,
      "alternative": "Alternative moins chère",
      "seasonal": true
    }}
  ],
  "total_estimated_cost": 45.0,
  "savings_tips": ["Conseil 1", "Conseil 2"],
  "recommended_stores": ["Marché central", "Super U"]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            optimization_data = self._parse_ai_response(response.text)
            return optimization_data
        except Exception as e:
            print(f"Erreur optimisation courses: {e}")
            return {'optimized_list': shopping_list, 'total_estimated_cost': 0}
    
    def analyze_nutritional_balance(self, meals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyse l'équilibre nutritionnel d'un planning"""
        
        meals_text = "\n".join([f"- {meal['recipe_name']} ({meal['main_ingredient']})" 
                               for meal in meals])
        
        prompt = f"""
Analyse l'équilibre nutritionnel de ce planning de repas camerounais :

{meals_text}

Évalue :
1. L'équilibre des macronutriments
2. La diversité des ingrédients
3. Les apports en vitamines/minéraux
4. Les recommandations d'amélioration

Format JSON :
{{
  "nutritional_score": 8.5,
  "macronutrients": {{
    "proteins": "Bon",
    "carbs": "Équilibré", 
    "fats": "À améliorer"
  }},
  "vitamins_minerals": {{
    "vitamin_c": "Excellent",
    "iron": "Bon",
    "calcium": "Moyen"
  }},
  "recommendations": [
    "Ajouter plus de légumes verts",
    "Inclure des fruits de saison"
  ],
  "health_benefits": [
    "Riche en protéines",
    "Bonne source de fibres"
  ]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            analysis_data = self._parse_ai_response(response.text)
            return analysis_data
        except Exception as e:
            print(f"Erreur analyse nutritionnelle: {e}")
            return {'nutritional_score': 0, 'recommendations': []}

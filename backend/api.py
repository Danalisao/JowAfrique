"""
API Flask refactorisée pour JowAfrique - Clean Architecture
Couches: API → Services → Database
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, date
import os
import sys

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(__file__))

from database import DatabaseManager
from services.meal_service import MealService
from services.plan_service import PlanService
from models import UserPreferences, CuisineType, BudgetLevel

app = Flask(__name__)
CORS(app)

# Initialisation des services
db_manager = DatabaseManager()
meal_service = MealService(db_manager)
plan_service = PlanService(db_manager)

def validate_required_fields(data: dict, required_fields: list) -> tuple[bool, str]:
    """Valide que tous les champs requis sont présents"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Champs manquants: {', '.join(missing_fields)}"
    return True, ""

def format_meal_response(meal_data: dict) -> dict:
    """Formate une réponse de repas pour l'API"""
    # Déterminer le type de repas basé sur meal_type
    meal_type_map = {
        'Petit-déjeuner': 'DÉJEUNER',
        'Déjeuner': 'DÉJEUNER', 
        'Dîner': 'DÎNER'
    }
    
    meal_type = meal_type_map.get(meal_data.get('meal_type', 'Dîner'), 'DÎNER')
    
    # Heure par défaut selon le type
    time_map = {
        'DÉJEUNER': '12:00',
        'DÎNER': '19:00'
    }
    
    return {
        'id': meal_data['id'],
        'type': meal_type,
        'time': time_map.get(meal_type, '19:00'),
        'name': meal_data['recipe_name'],
        'calories': f"{meal_data['prep_time'] * 10 + meal_data['cook_time'] * 5} kcal" if meal_data['prep_time'] and meal_data['cook_time'] else "N/A",
        'weight': f"{meal_data['prep_time'] * 15} gm" if meal_data['prep_time'] else "N/A",
        'image': meal_data['image_url'] or None,
        'isEditable': True,
        'jowId': meal_data['jow_recipe_id'],
        'url': meal_data['jow_recipe_url'],
        'videoUrl': meal_data.get('video_url'),
        'ingredient': meal_data['main_ingredient'],
        'cuisine': meal_data['cuisine_type'],
        'prepTime': meal_data['prep_time'],
        'cookTime': meal_data['cook_time'],
        'isFavorite': bool(meal_data['is_favorite']),
        'rating': meal_data['rating'] or 0,
        'notes': meal_data['notes'],
        'dayOfWeek': meal_data['day_of_week'],
        'mealType': meal_data.get('meal_type', 'Dîner')
    }

# ============================================================================
# ENDPOINTS PLANS
# ============================================================================

@app.route('/api/plans', methods=['GET'])
def get_plans():
    """Récupère tous les plans hebdomadaires"""
    try:
        plans_data = plan_service.get_plans()
        # Formater les plans pour correspondre au format frontend
        formatted_plans = []
        for plan in plans_data:
            formatted_plans.append({
                'id': plan['id'],
                'planName': plan['plan_name'],
                'weekStartDate': plan['week_start_date'],
                'totalBudgetEstimate': plan['total_budget_estimate'],
                'generatedByAi': bool(plan['generated_by_ai']),
                'createdAt': plan['created_at']
            })
        return jsonify(formatted_plans)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plans', methods=['POST'])
def create_plan():
    """Crée un nouveau plan hebdomadaire"""
    try:
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['planName', 'weekStartDate']
        is_valid, error_msg = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Conversion des préférences
        preferences_data = data.get('preferences', {})
        cuisines = [CuisineType(c) for c in preferences_data.get('cuisines', ['cameroun'])]
        budget = BudgetLevel(preferences_data.get('budget', 'modéré'))
        
        preferences = UserPreferences(
            cuisines=cuisines,
            budget=budget,
            light=preferences_data.get('light', False),
            vegetarian=preferences_data.get('vegetarian', False)
        )
        
        # Création du plan
        plan_id = plan_service.create_plan(
            data['planName'],
            date.fromisoformat(data['weekStartDate']),
            preferences,
            data.get('totalBudgetEstimate')
        )
        
        return jsonify({'id': plan_id, 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plans/<int:plan_id>', methods=['GET'])
def get_plan(plan_id):
    """Récupère un plan par son ID"""
    try:
        plan = plan_service.get_plan_by_id(plan_id)
        if not plan:
            return jsonify({'error': 'Plan non trouvé'}), 404
        return jsonify(plan)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    """Supprime un plan"""
    try:
        success = plan_service.delete_plan(plan_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Plan non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plans/<int:plan_id>/statistics', methods=['GET'])
def get_plan_statistics(plan_id):
    """Récupère les statistiques d'un plan"""
    try:
        stats = plan_service.get_plan_statistics(plan_id)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ENDPOINTS REPAS
# ============================================================================

@app.route('/api/plans/<int:plan_id>/meals', methods=['GET'])
def get_plan_meals(plan_id):
    """Récupère les repas d'un plan"""
    try:
        meals_data = meal_service.get_meals_by_plan(plan_id)
        meals = [format_meal_response(meal) for meal in meals_data]
        return jsonify(meals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plans/<int:plan_id>/meals', methods=['POST'])
def add_meal_to_plan(plan_id):
    """Ajoute un repas à un plan"""
    try:
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['dayOfWeek', 'mealType', 'name']
        is_valid, error_msg = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Préparation des données
        meal_data = {
            'plan_id': plan_id,
            'day_of_week': data['dayOfWeek'],
            'meal_type': data['mealType'],
            'recipe_name': data['name'],
            'jow_recipe_id': data.get('jowId'),
            'jow_recipe_url': data.get('url'),
            'main_ingredient': data.get('ingredient'),
            'cuisine_type': data.get('cuisine'),
            'image_url': data.get('image'),
            'video_url': data.get('videoUrl'),
            'prep_time': data.get('prepTime'),
            'cook_time': data.get('cookTime'),
            'is_favorite': data.get('isFavorite', False),
            'rating': data.get('rating', 0),
            'notes': data.get('notes')
        }
        
        meal_id = meal_service.add_meal(meal_data)
        return jsonify({'id': meal_id, 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    """Met à jour un repas"""
    try:
        data = request.get_json()
        
        # Champs modifiables
        allowed_fields = ['isFavorite', 'rating', 'notes']
        updates = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not updates:
            return jsonify({'error': 'Aucun champ valide à mettre à jour'}), 400
        
        success = meal_service.update_meal(meal_id, updates)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Repas non trouvé'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    """Supprime un repas"""
    try:
        success = meal_service.delete_meal(meal_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Repas non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meals', methods=['GET'])
def get_all_meals():
    """Récupère tous les repas"""
    try:
        meals_data = meal_service.get_all_meals()
        meals = [format_meal_response(meal) for meal in meals_data]
        return jsonify(meals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meals/<int:meal_id>/favorite', methods=['POST'])
def toggle_favorite(meal_id):
    """Bascule le statut favori d'un repas"""
    try:
        success = meal_service.toggle_favorite(meal_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Repas non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meals/<int:meal_id>/rate', methods=['POST'])
def rate_meal(meal_id):
    """Note un repas"""
    try:
        data = request.get_json()
        rating = data.get('rating')
        
        if not rating or not isinstance(rating, int) or not (1 <= rating <= 5):
            return jsonify({'error': 'Note invalide (1-5 requis)'}), 400
        
        success = meal_service.rate_meal(meal_id, rating)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Repas non trouvé'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/current-meal', methods=['GET'])
def get_current_meal():
    """Récupère le repas actuel"""
    try:
        meal_data = meal_service.get_current_meal()
        if meal_data:
            return jsonify(format_meal_response(meal_data))
        else:
            return jsonify({'error': 'Aucun repas trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ENDPOINTS STATISTIQUES
# ============================================================================

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Récupère les statistiques globales"""
    try:
        stats = db_manager.get_statistics()
        return jsonify({
            'totalPlans': stats.total_plans,
            'totalRecipes': stats.total_recipes,
            'favoriteRecipes': stats.favorite_recipes,
            'avgRating': stats.avg_rating,
            'topIngredients': stats.top_ingredients
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ENDPOINTS LISTE DE COURSES
# ============================================================================

@app.route('/api/plans/<int:plan_id>/shopping-list', methods=['GET'])
def get_shopping_list(plan_id):
    """Génère une liste de courses pour un plan"""
    try:
        ingredients = meal_service.generate_shopping_list(plan_id)
        return jsonify(ingredients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ENDPOINTS FAVORIS
# ============================================================================

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Récupère les favoris"""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT jow_recipe_id, recipe_name, main_ingredient, cuisine_type, 
                       image_url, added_date
                FROM favorites
                ORDER BY added_date DESC
            """)
            favorites = [dict(row) for row in cursor.fetchall()]
            return jsonify(favorites)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/favorites/<int:meal_id>', methods=['DELETE'])
def remove_from_favorites(meal_id):
    """Supprime un repas des favoris"""
    try:
        success = meal_service.remove_from_favorites(meal_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Favori non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de l'état de l'API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0'
    })

# ===== ENDPOINTS IA =====

@app.route('/api/ai/generate-plan', methods=['POST'])
def generate_ai_plan():
    """Génère un planning hebdomadaire avec Gemini AI"""
    try:
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['planName', 'weekStartDate', 'preferences']
        is_valid, error_msg = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Conversion des préférences
        preferences_data = data.get('preferences', {})
        cuisines = [CuisineType(c) for c in preferences_data.get('cuisines', ['cameroun'])]
        budget = BudgetLevel(preferences_data.get('budget', 'modéré'))
        
        preferences = UserPreferences(
            cuisines=cuisines,
            budget=budget,
            light=preferences_data.get('light', False),
            vegetarian=preferences_data.get('vegetarian', False)
        )
        
        # Génération du plan avec IA (utilise maintenant plan_service directement)
        result = plan_service.generate_ai_plan(
            preferences,
            data['planName'],
            date.fromisoformat(data['weekStartDate'])
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/meal-variations/<int:meal_id>', methods=['GET'])
def get_meal_variations(meal_id):
    """Suggère des variations d'un repas avec l'IA"""
    try:
        # Récupérer les préférences par défaut (à améliorer avec authentification)
        preferences = UserPreferences(
            cuisines=[CuisineType.CAMEROUN],
            budget=BudgetLevel.MODERATE,
            light=False,
            vegetarian=False
        )
        
        # Utiliser directement ai_service
        from services.ai_service import AIService
        ai_service = AIService()
        
        meal_data = db_manager.get_plan_meals(None)  # À adapter pour récupérer meal_id
        variations = ai_service.suggest_meal_variations(meal_data if meal_data else {}, preferences)
        
        return jsonify({
            'success': True,
            'variations': variations,
            'ai_model': 'gemini-2.0-flash'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/optimize-shopping/<int:plan_id>', methods=['POST'])
def optimize_shopping_list(plan_id):
    """Optimise la liste de courses avec l'IA"""
    try:
        data = request.get_json()
        budget = data.get('budget', 50.0)
        
        # Utiliser directement meal_service + ai_service
        from services.ai_service import AIService
        ai_service = AIService()
        
        shopping_list = meal_service.generate_shopping_list(plan_id)
        optimization = ai_service.generate_shopping_optimization(shopping_list, budget)
        
        return jsonify({
            'success': True,
            'optimization': optimization,
            'ai_model': 'gemini-2.0-flash'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/nutrition-analysis/<int:plan_id>', methods=['GET'])
def analyze_nutrition(plan_id):
    """Analyse l'équilibre nutritionnel d'un plan avec l'IA"""
    try:
        # Utiliser directement ai_service
        from services.ai_service import AIService
        ai_service = AIService()
        
        meals = meal_service.get_meals_by_plan(plan_id)
        analysis = ai_service.analyze_nutritional_balance(meals)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'ai_model': 'gemini-2.0-flash'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/regenerate-day/<int:plan_id>', methods=['POST'])
def regenerate_plan_day(plan_id):
    """Régénère les repas d'un jour spécifique avec l'IA"""
    try:
        data = request.get_json()
        day_of_week = data.get('day_of_week')
        
        if not day_of_week:
            return jsonify({'error': 'day_of_week requis'}), 400
        
        # Préférences par défaut
        preferences = UserPreferences(
            cuisines=[CuisineType.CAMEROUN],
            budget=BudgetLevel.MODERATE,
            light=False,
            vegetarian=False
        )
        
        # Récupérer les repas du jour et les supprimer
        meals = meal_service.get_meals_by_plan(plan_id)
        for meal in meals:
            if meal['day_of_week'] == day_of_week:
                meal_service.delete_meal(meal['id'])
        
        # Générer de nouveaux repas (logique simplifiée)
        from services.hybrid_recipe_service import HybridRecipeService
        hybrid_service = HybridRecipeService(db_manager)
        
        # Générer une recette pour le jour
        weekly_recipes = hybrid_service.generate_weekly_plan_recipes(preferences, plan_id)
        day_meals = [r for r in weekly_recipes if r.get('day_of_week') == day_of_week]
        
        added_count = 0
        for meal_data in day_meals:
            meal_service.add_meal(meal_data)
            added_count += 1
        
        return jsonify({
            'success': True,
            'day_of_week': day_of_week,
            'meals_added': added_count,
            'ai_model': 'gemini-2.0-flash'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Demarrage de l'API JowAfrique sur http://localhost:5000")
    print("Frontend Next.js: http://localhost:3000")
    app.run(host='0.0.0.0', port=5000, debug=True)

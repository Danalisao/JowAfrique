"""
Script d'initialisation des recettes camerounaises en base de données
"""
import sys
import os
from datetime import date

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(__file__) + '/..')

from database import DatabaseManager
from services.meal_service import MealService
from models import CuisineType, MealType

def init_cameroon_recipes():
    """Initialise les recettes camerounaises en base de données"""
    
    # Initialisation des services
    db_manager = DatabaseManager("jowafrique.db")
    meal_service = MealService(db_manager)
    
    print("Initialisation des recettes camerounaises...")
    
    # Recettes camerounaises authentiques
    cameroon_recipes = [
        {
            'recipe_name': 'Ndolé',
            'main_ingredient': 'Arachides',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400',
            'prep_time': 45,
            'cook_time': 60,
            'notes': 'Plat national du Cameroun aux arachides et légumes',
            'is_favorite': True,
            'rating': 5,
            'tags': ['traditionnel', 'national', 'arachides', 'légumes']
        },
        {
            'recipe_name': 'Poulet DG',
            'main_ingredient': 'Poulet',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400',
            'prep_time': 30,
            'cook_time': 45,
            'notes': 'Poulet sauté aux légumes, spécialité camerounaise',
            'is_favorite': True,
            'rating': 5,
            'tags': ['poulet', 'légumes', 'sauté', 'populaire']
        },
        {
            'recipe_name': 'Riz au gras',
            'main_ingredient': 'Riz',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400',
            'prep_time': 20,
            'cook_time': 30,
            'notes': 'Riz parfumé aux légumes et épices',
            'is_favorite': False,
            'rating': 4,
            'tags': ['riz', 'légumes', 'épices', 'accompagnement']
        },
        {
            'recipe_name': 'Eru',
            'main_ingredient': 'Eru',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400',
            'prep_time': 40,
            'cook_time': 50,
            'notes': 'Plat aux feuilles d\'eru et poisson fumé',
            'is_favorite': True,
            'rating': 5,
            'tags': ['eru', 'poisson', 'feuilles', 'traditionnel']
        },
        {
            'recipe_name': 'Koki',
            'main_ingredient': 'Haricots',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400',
            'prep_time': 60,
            'cook_time': 90,
            'notes': 'Haricots pilés cuits dans des feuilles de bananier',
            'is_favorite': False,
            'rating': 4,
            'tags': ['haricots', 'feuilles', 'traditionnel', 'végétarien']
        },
        {
            'recipe_name': 'Achu',
            'main_ingredient': 'Taro',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400',
            'prep_time': 30,
            'cook_time': 45,
            'notes': 'Taro pilé avec sauce aux arachides',
            'is_favorite': False,
            'rating': 4,
            'tags': ['taro', 'arachides', 'pilé', 'traditionnel']
        },
        {
            'recipe_name': 'Nkui',
            'main_ingredient': 'Épinards',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400',
            'prep_time': 25,
            'cook_time': 35,
            'notes': 'Épinards aux arachides et poisson',
            'is_favorite': False,
            'rating': 3,
            'tags': ['épinards', 'arachides', 'poisson', 'légumes']
        },
        {
            'recipe_name': 'Poulet braisé',
            'main_ingredient': 'Poulet',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400',
            'prep_time': 15,
            'cook_time': 50,
            'notes': 'Poulet mariné et grillé aux épices',
            'is_favorite': True,
            'rating': 5,
            'tags': ['poulet', 'grillé', 'épices', 'mariné']
        },
        {
            'recipe_name': 'Poisson braisé',
            'main_ingredient': 'Poisson',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400',
            'prep_time': 20,
            'cook_time': 30,
            'notes': 'Poisson grillé aux épices et légumes',
            'is_favorite': True,
            'rating': 4,
            'tags': ['poisson', 'grillé', 'épices', 'légumes']
        },
        {
            'recipe_name': 'Plantain mûr',
            'main_ingredient': 'Plantain',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400',
            'prep_time': 10,
            'cook_time': 20,
            'notes': 'Plantain mûr grillé ou frit',
            'is_favorite': False,
            'rating': 3,
            'tags': ['plantain', 'grillé', 'frit', 'accompagnement']
        },
        {
            'recipe_name': 'Taro aux épinards',
            'main_ingredient': 'Taro',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400',
            'prep_time': 25,
            'cook_time': 40,
            'notes': 'Taro aux épinards et arachides',
            'is_favorite': False,
            'rating': 4,
            'tags': ['taro', 'épinards', 'arachides', 'végétarien']
        },
        {
            'recipe_name': 'Kati-kati',
            'main_ingredient': 'Poulet',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400',
            'prep_time': 20,
            'cook_time': 35,
            'notes': 'Poulet grillé aux épices et oignons',
            'is_favorite': True,
            'rating': 4,
            'tags': ['poulet', 'grillé', 'épices', 'oignons']
        },
        {
            'recipe_name': 'Soupe de poisson',
            'main_ingredient': 'Poisson',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400',
            'prep_time': 30,
            'cook_time': 45,
            'notes': 'Soupe traditionnelle au poisson et légumes',
            'is_favorite': False,
            'rating': 4,
            'tags': ['poisson', 'soupe', 'légumes', 'traditionnel']
        },
        {
            'recipe_name': 'Beignets de haricots',
            'main_ingredient': 'Haricots',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400',
            'prep_time': 40,
            'cook_time': 20,
            'notes': 'Beignets de haricots frits, spécialité camerounaise',
            'is_favorite': False,
            'rating': 3,
            'tags': ['haricots', 'beignets', 'frit', 'snack']
        },
        {
            'recipe_name': 'Puff-puff',
            'main_ingredient': 'Farine',
            'cuisine_type': CuisineType.CAMEROUN.value,
            'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400',
            'prep_time': 30,
            'cook_time': 15,
            'notes': 'Beignets sucrés traditionnels',
            'is_favorite': False,
            'rating': 3,
            'tags': ['farine', 'beignets', 'sucré', 'dessert']
        }
    ]
    
    # Ajouter les recettes en base
    added_count = 0
    for recipe in cameroon_recipes:
        try:
            # Ajouter comme recette de base (sans plan_id)
            recipe_data = {
                'recipe_name': recipe['recipe_name'],
                'main_ingredient': recipe['main_ingredient'],
                'cuisine_type': recipe['cuisine_type'],
                'image_url': recipe['image_url'],
                'prep_time': recipe['prep_time'],
                'cook_time': recipe['cook_time'],
                'notes': recipe['notes'],
                'is_favorite': recipe['is_favorite'],
                'rating': recipe['rating'],
                'jow_recipe_id': None,  # Recettes locales
                'jow_recipe_url': None,
                'meal_type': MealType.DINNER.value,
                'day_of_week': None,  # Pas assigné à un jour
                'plan_id': None  # Pas assigné à un plan
            }
            
            recipe_id = meal_service.add_meal(recipe_data)
            if recipe_id:
                added_count += 1
                print(f"+ Recette ajoutee: {recipe['recipe_name']}")
            else:
                print(f"- Erreur ajout: {recipe['recipe_name']}")
                
        except Exception as e:
            print(f"- Erreur {recipe['recipe_name']}: {e}")
    
    print(f"\nInitialisation terminée!")
    print(f"Recettes camerounaises ajoutées: {added_count}/{len(cameroon_recipes)}")
    
    return added_count

if __name__ == "__main__":
    init_cameroon_recipes()

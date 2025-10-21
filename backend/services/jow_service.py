"""
Service d'intégration avec l'API Jow via la librairie officielle
"""
from typing import List, Dict, Any, Optional
from jow_api import Jow

class JowService:
    def __init__(self):
        """Initialise le service Jow API avec la librairie officielle"""
        pass
    
    def search_recipes(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recherche des recettes sur Jow"""
        try:
            recipes = Jow.search(query, limit=limit)
            return self._format_jow_recipes(recipes)
            
        except Exception as e:
            print(f"Erreur recherche Jow: {e}")
            return []
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une recette spécifique par ID (utilise la recherche)"""
        try:
            # Recherche par ID ou nom
            recipes = Jow.search(recipe_id, limit=1)
            if recipes:
                return self._format_jow_recipe(recipes[0])
            return None
            
        except Exception as e:
            print(f"Erreur récupération recette Jow {recipe_id}: {e}")
            return None
    
    def get_recipes_by_cuisine(self, cuisine: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupère des recettes par type de cuisine"""
        try:
            # Recherche par cuisine
            recipes = Jow.search(f"{cuisine} cuisine", limit=limit)
            return self._format_jow_recipes(recipes)
            
        except Exception as e:
            print(f"Erreur récupération cuisine Jow {cuisine}: {e}")
            return []
    
    def get_recipe_suggestions(self, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Récupère des suggestions de recettes basées sur les préférences"""
        try:
            # Construire une requête de recherche basée sur les préférences
            query_parts = []
            
            # Ajouter les cuisines
            jow_cuisines = self._map_cuisines_to_jow(preferences.get('cuisines', []))
            if jow_cuisines:
                query_parts.extend(jow_cuisines)
            
            # Ajouter des filtres selon les préférences
            if preferences.get('vegetarian'):
                query_parts.append("vegetarian")
            if preferences.get('light'):
                query_parts.append("light")
            
            # Construire la requête
            query = " ".join(query_parts) if query_parts else "recettes"
            
            recipes = Jow.search(query, limit=20)
            return self._format_jow_recipes(recipes)
            
        except Exception as e:
            print(f"Erreur suggestions Jow: {e}")
            return []
    
    def _format_jow_recipes(self, recipes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formate les recettes Jow pour notre format"""
        formatted_recipes = []
        
        for recipe in recipes:
            formatted_recipe = self._format_jow_recipe(recipe)
            if formatted_recipe:
                formatted_recipes.append(formatted_recipe)
        
        return formatted_recipes
    
    def _format_jow_recipe(self, recipe) -> Optional[Dict[str, Any]]:
        """Formate une recette Jow individuelle"""
        try:
            return {
                'jow_recipe_id': getattr(recipe, 'id', None),
                'jow_recipe_url': getattr(recipe, 'url', None),
                'recipe_name': getattr(recipe, 'name', ''),
                'description': getattr(recipe, 'description', ''),
                'image_url': getattr(recipe, 'imageUrl', None),
                'prep_time': getattr(recipe, 'preparationTime', 0) or 0,
                'cook_time': getattr(recipe, 'cookingTime', 0) or 0,
                'total_time': (getattr(recipe, 'preparationTime', 0) or 0) + (getattr(recipe, 'cookingTime', 0) or 0),
                'servings': getattr(recipe, 'coversCount', 1),
                'difficulty': 'medium',  # Pas disponible dans JowResult
                'cuisine_type': 'international',  # Pas disponible dans JowResult
                'main_ingredient': self._extract_main_ingredient(recipe),
                'ingredients': getattr(recipe, 'ingredients', []),
                'instructions': [],  # Pas disponible dans JowResult
                'nutrition': {},  # Pas disponible dans JowResult
                'tags': [],  # Pas disponible dans JowResult
                'rating': 0,  # Pas disponible dans JowResult
                'source': 'jow'
            }
        except Exception as e:
            print(f"Erreur formatage recette Jow: {e}")
            return None
    
    def _extract_main_ingredient(self, recipe) -> str:
        """Extrait l'ingrédient principal d'une recette Jow"""
        ingredients = getattr(recipe, 'ingredients', [])
        if not ingredients:
            return 'Divers'
        
        # Prendre le premier ingrédient comme principal
        first_ingredient = ingredients[0]
        if hasattr(first_ingredient, 'name'):
            return first_ingredient.name
        elif isinstance(first_ingredient, dict):
            return first_ingredient.get('name', 'Divers')
        elif isinstance(first_ingredient, str):
            return first_ingredient.split(',')[0].strip()
        
        return 'Divers'
    
    def _map_cuisines_to_jow(self, cuisines: List[str]) -> List[str]:
        """Mappe nos types de cuisine vers les cuisines Jow"""
        cuisine_mapping = {
            'cameroun': 'african',
            'asiatique': 'asian',
            'mexican': 'mexican',
            'french': 'french',
            'italian': 'italian',
            'indian': 'indian',
            'mediterranean': 'mediterranean'
        }
        
        jow_cuisines = []
        for cuisine in cuisines:
            jow_cuisine = cuisine_mapping.get(cuisine.lower())
            if jow_cuisine:
                jow_cuisines.append(jow_cuisine)
        
        return jow_cuisines
    
    @property
    def _cuisine_mapping(self):
        """Mapping des cuisines pour Jow"""
        return {
            'cameroun': 'african',
            'asiatique': 'asian',
            'mexican': 'mexican',
            'french': 'french',
            'italian': 'italian',
            'indian': 'indian',
            'mediterranean': 'mediterranean'
        }
    
    def get_available_cuisines(self) -> List[str]:
        """Récupère les cuisines disponibles sur Jow"""
        # Retourner les cuisines mappées
        return list(self._cuisine_mapping.keys())
    
    def test_connection(self) -> bool:
        """Teste la connexion à l'API Jow"""
        try:
            # Test simple avec une recherche
            recipes = Jow.search("test", limit=1)
            return isinstance(recipes, list)
        except Exception as e:
            print(f"Erreur test connexion Jow: {e}")
            return False

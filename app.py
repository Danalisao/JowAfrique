import streamlit as st
from jow_api import Jow
import time
from typing import List, Dict
import sqlite3
import os
from datetime import datetime
import google.generativeai as genai

# Configuration de Gemini AI
GEMINI_API_KEY = "AIzaSyBUysypCabOFa7Nw8hhKYZISiLemk_-kAk"
genai.configure(api_key=GEMINI_API_KEY)

# Configuration de la page
st.set_page_config(
    page_title="Recettes Jow - Fusion Afrique-Europe",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonctions de base de données
def get_db_connection():
    """Établit une connexion à la base de données SQLite"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'jowafrique.db')
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données: {str(e)}")
        return None

def init_database():
    """Initialise la base de données avec les tables nécessaires"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Créer la table favorites
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id TEXT NOT NULL,
                    recipe_name TEXT NOT NULL,
                    recipe_url TEXT,
                    recipe_description TEXT,
                    preparation_time INTEGER,
                    cooking_time INTEGER,
                    covers_count INTEGER,
                    ingredients_data TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(recipe_id)
                )
            """)
            
            # Créer la table search_history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    search_query TEXT NOT NULL,
                    search_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    results_count INTEGER DEFAULT 0
                )
            """)
            
            # Créer la table african_recipes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS african_recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    ingredients TEXT,
                    preparation_steps TEXT,
                    preparation_time INTEGER,
                    cooking_time INTEGER,
                    serves INTEGER,
                    country_origin TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Créer les index
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_history_date ON search_history(search_date DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_favorites_created ON favorites(created_at DESC)")
            
            # Vérifier si la table african_recipes est vide et la peupler
            cursor.execute("SELECT COUNT(*) FROM african_recipes")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insérer les recettes africaines par défaut
                african_recipes_data = [
                    ('Poulet Yassa', 'Plat sénégalais emblématique de poulet mariné aux oignons et citron', 
                     'Poulet (1kg), Oignons (4 gros), Citrons (3), Moutarde (2 c.à.s), Huile, Ail (3 gousses), Piment, Bouillon cube, Riz blanc',
                     '1. Mariner le poulet avec citron, oignons, ail, moutarde pendant 2h. 2. Griller le poulet. 3. Faire revenir les oignons marinés jusqu\'à caramélisation. 4. Ajouter le poulet et mijoter 20 min. 5. Servir avec du riz blanc.',
                     30, 45, 6, 'Sénégal'),
                    
                    ('Riz Jollof', 'Riz épicé ouest-africain cuit dans une sauce tomate parfumée',
                     'Riz (500g), Tomates (4), Oignon (2), Pâte de tomate (3 c.à.s), Huile végétale, Ail, Gingembre, Thym, Curry, Piment, Bouillon cube, Poivrons',
                     '1. Mixer les tomates, oignons, ail, gingembre. 2. Faire revenir dans l\'huile. 3. Ajouter pâte de tomate et épices. 4. Incorporer le riz et le bouillon. 5. Cuire à feu doux 30-40 min.',
                     20, 40, 8, 'Nigéria/Ghana'),
                    
                    ('Thiéboudienne', 'Plat national sénégalais: riz au poisson et légumes',
                     'Poisson frais (1kg), Riz brisé (1kg), Tomate concentrée, Poisson séché, Chou, Carottes, Aubergines, Manioc, Patate douce, Navet, Gombo, Yet (coquillage), Huile, Piment, Ail, Persil',
                     '1. Farcir le poisson avec persil, ail, piment. 2. Préparer la sauce tomate. 3. Cuire le poisson et les légumes. 4. Cuire le riz dans le bouillon. 5. Servir ensemble.',
                     40, 60, 10, 'Sénégal'),
                    
                    ('Mafé', 'Ragoût ouest-africain onctueux à la pâte d\'arachide',
                     'Viande (bœuf/poulet 1kg), Pâte d\'arachide (300g), Tomates (3), Oignons (2), Pâte de tomate, Carottes, Chou, Patate douce, Aubergine, Ail, Gingembre, Piment, Huile, Bouillon',
                     '1. Faire revenir la viande. 2. Ajouter oignons, tomates, épices. 3. Incorporer la pâte d\'arachide diluée. 4. Ajouter les légumes. 5. Mijoter 45 min. Servir avec riz.',
                     25, 60, 6, 'Mali/Sénégal'),
                    
                    ('Ndolé', 'Plat national camerounais aux feuilles de ndolé et arachides',
                     'Feuilles de ndolé (500g), Arachides grillées (200g), Viande/Poisson/Crevettes, Oignons, Ail, Gingembre, Piment, Huile de palme, Cube Maggi',
                     '1. Faire bouillir les feuilles ndolé plusieurs fois. 2. Moudre les arachides. 3. Faire revenir viande et aromates. 4. Ajouter feuilles et pâte d\'arachide. 5. Mijoter 30 min. Servir avec plantain/bâton de manioc.',
                     30, 45, 6, 'Cameroun'),
                    
                    ('Attiéké Poisson', 'Semoule de manioc fermenté avec poisson frit et sauce tomate épicée',
                     'Attiéké (500g), Poisson (thon/maquereau), Tomates (4), Oignons (2), Piment, Ail, Gingembre, Huile, Citron, Persil',
                     '1. Assaisonner et frire le poisson. 2. Préparer sauce tomate avec oignons, piment, ail. 3. Cuire l\'attiéké à la vapeur. 4. Servir avec poisson frit et sauce.',
                     20, 25, 4, 'Côte d\'Ivoire'),
                    
                    ('Sauce Gombo', 'Sauce gluante traditionnelle aux gombos frais',
                     'Gombo frais (500g), Viande/Poisson fumé, Tomates, Oignons, Huile de palme, Piment, Ail, Cubes Maggi, Sel',
                     '1. Couper les gombos en morceaux. 2. Préparer sauce tomate. 3. Ajouter gombo et cuire. 4. Incorporer viande/poisson. 5. Mijoter jusqu\'à texture gluante. Servir avec foufou.',
                     15, 30, 4, 'Bénin/Togo'),
                    
                    ('Foufou Igname', 'Pâte d\'igname pilée, accompagnement de base',
                     'Igname (1kg), Eau, Sel',
                     '1. Éplucher et couper l\'igname. 2. Faire bouillir jusqu\'à tendre. 3. Piler énergiquement en ajoutant un peu d\'eau. 4. Former une boule lisse et élastique. Servir avec sauce.',
                     15, 25, 4, 'Ghana/Nigéria'),
                    
                    ('Kedjenou', 'Poulet mijoté ivoirien aux légumes dans sa propre eau',
                     'Poulet (1 entier), Oignons (2), Tomates (3), Aubergines, Gingembre, Ail, Piment, Sel, Poivre',
                     '1. Découper le poulet. 2. Mettre tous ingrédients dans canari hermétique. 3. Sceller et faire mijoter 45 min en secouant régulièrement. 4. Servir avec attiéké ou riz.',
                     20, 50, 6, 'Côte d\'Ivoire'),
                    
                    ('Poisson Braisé', 'Poisson grillé mariné aux épices africaines',
                     'Poisson entier (bar/carpe/tilapia), Oignon, Tomate, Piment, Gingembre, Ail, Citron, Huile, Cube Maggi, Poivre, Sel',
                     '1. Vider et nettoyer le poisson. 2. Mariner avec oignon, ail, gingembre, piment, citron 1h. 3. Griller au feu de bois ou four. 4. Servir avec sauce tomate oignon pimentée.',
                     20, 30, 2, 'Afrique de l\'Ouest')
                ]
                
                cursor.executemany("""
                    INSERT INTO african_recipes 
                    (name, description, ingredients, preparation_steps, preparation_time, cooking_time, serves, country_origin)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, african_recipes_data)
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Erreur lors de l'initialisation de la base de données: {str(e)}")
            if conn:
                conn.close()
            return False
    return False

def save_to_favorites(recipe_id, recipe_name, recipe_url, recipe_description, prep_time, cook_time, covers, ingredients=None):
    """Sauvegarde une recette dans les favoris"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Sérialiser les ingrédients en texte
            ingredients_text = ""
            if ingredients:
                ingredients_text = "|".join([f"{ing.name}:{ing.quantity or ''} {ing.unit or ''}".strip() 
                                             for ing in ingredients if hasattr(ing, 'name')])
            
            cursor.execute("""
                INSERT INTO favorites (recipe_id, recipe_name, recipe_url, recipe_description, 
                                      preparation_time, cooking_time, covers_count, ingredients_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (recipe_id) DO NOTHING
            """, (recipe_id, recipe_name, recipe_url, recipe_description, prep_time, cook_time, covers, ingredients_text))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde: {str(e)}")
            conn.close()
            return False
    return False

def remove_from_favorites(recipe_id):
    """Retire une recette des favoris"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM favorites WHERE recipe_id = ?", (recipe_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {str(e)}")
            conn.close()
            return False
    return False

def is_favorite(recipe_id):
    """Vérifie si une recette est dans les favoris"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM favorites WHERE recipe_id = ?", (recipe_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count > 0
        except Exception as e:
            conn.close()
            return False
    return False

def get_all_favorites():
    """Récupère toutes les recettes favorites"""
    conn = get_db_connection()
    favorites = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT recipe_id, recipe_name, recipe_url, recipe_description, 
                       preparation_time, cooking_time, covers_count, created_at, ingredients_data
                FROM favorites ORDER BY created_at DESC
            """)
            favorites = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Erreur lors de la récupération des favoris: {str(e)}")
            conn.close()
    return favorites

def save_search_history(query, results_count):
    """Enregistre une recherche dans l'historique"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO search_history (search_query, results_count)
                VALUES (?, ?)
            """, (query, results_count))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            conn.close()

def get_search_recommendations():
    """Récupère les recommandations basées sur l'historique"""
    conn = get_db_connection()
    recommendations = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT search_query, COUNT(*) as frequency
                FROM search_history
                WHERE search_date >= datetime('now', '-30 days')
                GROUP BY search_query
                ORDER BY frequency DESC, MAX(search_date) DESC
                LIMIT 5
            """)
            recommendations = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
        except Exception as e:
            conn.close()
    return recommendations

def get_african_recipes(search_query=None):
    """Récupère les recettes africaines de la base de données"""
    conn = get_db_connection()
    recipes = []
    if conn:
        try:
            cursor = conn.cursor()
            if search_query:
                cursor.execute("""
                    SELECT id, name, description, ingredients, preparation_steps, 
                           preparation_time, cooking_time, serves, country_origin
                    FROM african_recipes
                    WHERE LOWER(name) LIKE ? OR LOWER(ingredients) LIKE ? OR LOWER(description) LIKE ?
                    ORDER BY name
                """, (f'%{search_query.lower()}%', f'%{search_query.lower()}%', f'%{search_query.lower()}%'))
            else:
                cursor.execute("""
                    SELECT id, name, description, ingredients, preparation_steps, 
                           preparation_time, cooking_time, serves, country_origin
                    FROM african_recipes
                    ORDER BY name
                """)
            recipes = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Erreur lors de la récupération des recettes africaines: {str(e)}")
            conn.close()
    return recipes

def generer_liste_courses(recipe_ids):
    """Génère une liste de courses à partir des recettes favorites"""
    conn = get_db_connection()
    recipes_data = []
    
    if conn:
        try:
            cursor = conn.cursor()
            placeholders = ','.join(['?'] * len(recipe_ids))
            cursor.execute(f"""
                SELECT recipe_name, ingredients_data FROM favorites 
                WHERE recipe_id IN ({placeholders})
            """, tuple(recipe_ids))
            
            recipes_data = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Erreur lors de la génération de la liste: {str(e)}")
            if conn:
                conn.close()
    
    return recipes_data

def export_shopping_list_text(recipes_data):
    """Génère un texte exportable pour la liste de courses"""
    text = "📋 LISTE DE COURSES - RECETTES JOW\n"
    text += "=" * 50 + "\n\n"
    text += f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    text += f"🍽️ RECETTES SÉLECTIONNÉES ({len(recipes_data)}):\n"
    text += "=" * 50 + "\n\n"
    
    all_ingredients = {}
    
    for idx, (recipe_name, ingredients_data) in enumerate(recipes_data, 1):
        text += f"{idx}. {recipe_name}\n"
        
        # Parser les ingrédients
        if ingredients_data:
            text += "   Ingrédients:\n"
            ingredients = ingredients_data.split('|')
            for ing in ingredients:
                if ing.strip():
                    if ':' in ing:
                        name, quantity = ing.split(':', 1)
                        text += f"   • {name.strip()}: {quantity.strip()}\n"
                        
                        # Ajouter à la liste globale
                        ing_name = name.strip().lower()
                        if ing_name not in all_ingredients:
                            all_ingredients[ing_name] = []
                        all_ingredients[ing_name].append(quantity.strip())
                    else:
                        text += f"   • {ing.strip()}\n"
                        ing_name = ing.strip().lower()
                        if ing_name not in all_ingredients:
                            all_ingredients[ing_name] = []
        else:
            text += "   ⚠️ Ingrédients non disponibles - Consulte la recette sur Jow.fr\n"
        
        text += "\n"
    
    # Ajouter une liste consolidée des ingrédients
    if all_ingredients:
        text += "=" * 50 + "\n"
        text += "🛒 LISTE DE COURSES CONSOLIDÉE:\n"
        text += "-" * 50 + "\n"
        
        for ingredient_name, quantities in sorted(all_ingredients.items()):
            if quantities:
                text += f"• {ingredient_name.title()}"
                if quantities[0]:  # Si il y a des quantités
                    text += f" ({', '.join(quantities)})"
                text += "\n"
    
    text += "\n" + "=" * 50 + "\n"
    text += "💡 Conseil: Ajuste les quantités selon tes besoins!\n"
    text += "\n🌍 Bon appétit! 🍽️\n"
    
    return text

# Dictionnaire de substitutions pour ingrédients africains
SUBSTITUTIONS_AFRICAINES = {
    "manioc": "pommes de terre",
    "igname": "patate douce",
    "plantain": "banane",
    "gombo": "courgette",
    "foufou": "purée de pommes de terre",
    "yam": "patate douce",
    "cassava": "pommes de terre",
    "taro": "pommes de terre",
    "eddoe": "pommes de terre",
    "breadfruit": "pommes de terre",
    "scotch bonnet": "piment rouge",
    "palm oil": "huile d'olive",
    "palm nut": "noix de coco",
    "kola nut": "noix",
    "bitter leaf": "épinards",
    "uziza": "basilic",
    "ogbono": "graines de sésame",
    "locust beans": "sauce soja",
    "fermented fish": "sauce worcestershire",
    "dried fish": "sardines",
    "stock fish": "morue",
    "suya spice": "paprika fumé",
    "maggi": "bouillon cube",
    "attieke": "couscous",
    "gari": "semoule",
    "fufu": "purée de pommes de terre",
    "banku": "polenta",
    "kenkey": "polenta"
}

# Suggestions de fusion humoristiques
SUGGESTIONS_FUSION = [
    "Et si tu essayais une version sénégalaise de cette quiche 🥧 ? Ajoute un peu de thiéboudienne dedans !",
    "Cette recette ferait un malheur avec une touche de yassa 🍋 !",
    "Imagine cette soupe avec des épices de jollof rice 🌶️ - explosif !",
    "Cette pâtisserie + un soupçon de coco africain = délice garanti 🥥 !",
    "Et pourquoi pas transformer ce plat en version 'mafé' ? 🥜",
    "Cette salade avec des plantains frits sur le côté... Mmm ! 🍌",
    "Ce dessert revisité façon bissap-framboise ? Génial ! 🌺",
    "Ajoute du piment scotch bonnet (avec modération) pour réveiller ça ! 🌶️",
    "Version africaine : remplace par de l'huile de palme rouge ! 🔴",
    "Et si on y mettait des feuilles de manioc ? Révolutionnaire ! 🌿"
]

# Recettes africaines suggérées
RECETTES_AFRICAINES_SUGGEREES = [
    "Poulet yassa",
    "Riz jollof",
    "Poisson braisé",
    "Sauce gombo",
    "Foufou yam",
    "Thiéboudienne",
    "Mafé",
    "Attiéké poisson",
    "Ndolé",
    "Kedjenou"
]

def afficher_titre_principal():
    """Affiche le titre principal avec émojis africains"""
    st.title("🍽️ Recettes Jow - Fusion Afrique-Europe")
    st.markdown("### Découvre des recettes inspirantes et crée tes propres fusions culinaires ! 🌍✨")
    st.divider()

def afficher_sidebar():
    """Affiche la sidebar avec les suggestions africaines"""
    with st.sidebar:
        # Onglets pour organiser les sections
        tab1, tab2, tab3 = st.tabs(["🍲 Suggestions", "❤️ Favoris", "📊 Recommandations"])
        
        with tab1:
            st.header("🌍 Recettes Africaines")
            st.markdown("Clique pour rechercher :")
            
            for recette in RECETTES_AFRICAINES_SUGGEREES:
                if st.button(f"🍲 {recette}", key=f"suggestion_{recette}", width='stretch'):
                    st.session_state.search_query = recette
                    st.rerun()
        
        with tab2:
            st.header("❤️ Mes Favoris")
            favorites = get_all_favorites()
            
            if favorites:
                st.write(f"**{len(favorites)} recette(s) favorite(s)**")
                
                # Bouton pour exporter la liste de courses
                if st.button("📋 Exporter liste de courses", type="primary", width='stretch'):
                    recipe_ids = [fav[0] for fav in favorites]
                    recipes_data = generer_liste_courses(recipe_ids)
                    shopping_text = export_shopping_list_text(recipes_data)
                    
                    st.download_button(
                        label="💾 Télécharger la liste",
                        data=shopping_text,
                        file_name=f"liste_courses_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        width='stretch'
                    )
                
                st.divider()
                
                for fav in favorites:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        if st.button(fav[1][:30] + "...", key=f"fav_view_{fav[0]}", width='stretch'):
                            if fav[2]:  # Si URL disponible
                                st.markdown(f"🔗 [Voir la recette]({fav[2]})")
                            st.write(fav[3] if fav[3] else "")
                    with col2:
                        if st.button("🗑️", key=f"fav_del_{fav[0]}"):
                            remove_from_favorites(fav[0])
                            st.rerun()
            else:
                st.info("Aucun favori pour le moment. Ajoute des recettes en cliquant sur 🤍!")
        
        with tab3:
            st.header("📊 Tes recherches populaires")
            recommendations = get_search_recommendations()
            
            if recommendations:
                st.write("Basé sur ton historique :")
                for rec in recommendations:
                    if st.button(f"🔍 {rec}", key=f"rec_{rec}", width='stretch'):
                        st.session_state.search_query = rec
                        st.rerun()
            else:
                st.info("Effectue quelques recherches pour voir tes recommandations personnalisées !")
        
        st.divider()
        
        # Mode découverte
        st.header("🎭 Mode Découverte")
        mode_decouverte = st.toggle("Activer fusion Afrique-Europe", value=True)
        st.session_state.mode_decouverte = mode_decouverte
        
        if mode_decouverte:
            st.success("Mode fusion activé ! 🎉")
            st.info("Les suggestions de fusion apparaîtront avec tes résultats !")

def enrichir_recherche_avec_ia(query: str) -> Dict[str, any]:
    """Utilise Gemini pour analyser et enrichir la recherche de recettes africaines"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""Tu es un assistant culinaire spécialisé dans les recettes africaines.
        
Requête de recherche: "{query}"
        
Analyse cette requête et réponds en JSON avec:
        {{
            "est_africain": true/false (si la recherche concerne une recette africaine ou des ingrédients africains),
            "suggestions_recherche": [liste de 2-3 termes de recherche optimisés pour trouver des recettes africaines ou similaires],
            "ingredients_cles": [liste des ingrédients africains principaux liés à cette recherche],
            "conseil": "un conseil court pour adapter/africaniser la recette"
        }}
        
Réponds UNIQUEMENT avec le JSON, sans texte additionnel."""
        
        response = model.generate_content(prompt)
        
        # Parser la réponse JSON
        import json
        result_text = response.text.strip()
        # Retirer les balises markdown si présentes
        if result_text.startswith('```'):
            result_text = result_text.split('\n', 1)[1]
            result_text = result_text.rsplit('\n', 1)[0]
            if result_text.endswith('```'):
                result_text = result_text[:-3]
        
        result = json.loads(result_text)
        return result
    except Exception as e:
        st.warning(f"ℹ️ L'IA n'a pas pu analyser la recherche: {str(e)}")
        return {
            "est_africain": False,
            "suggestions_recherche": [query],
            "ingredients_cles": [],
            "conseil": ""
        }

def obtenir_substitution(ingredient: str) -> str:
    """Trouve une substitution pour un ingrédient africain"""
    ingredient_lower = ingredient.lower()
    for africain, europeen in SUBSTITUTIONS_AFRICAINES.items():
        if africain in ingredient_lower:
            return europeen
    return ingredient

def rechercher_avec_substitution(query: str) -> List:
    """Recherche avec substitution automatique si nécessaire"""
    try:
        # Première tentative avec la requête originale
        recipes = Jow.search(query, limit=10)
        return recipes, query, False
    except Exception as e:
        st.error(f"Erreur lors de la recherche : {str(e)}")
        return [], query, False

def rechercher_recettes_alternatives(query: str) -> List:
    """Recherche des recettes alternatives avec substitutions"""
    substitution = obtenir_substitution(query)
    if substitution != query.lower():
        try:
            recipes = Jow.search(substitution, limit=8)
            return recipes, substitution, True
        except Exception as e:
            st.error(f"Erreur lors de la recherche alternative : {str(e)}")
            return [], substitution, True
    return [], query, False

def afficher_carte_recette(recipe, col, est_substitution=False):
    """Affiche une carte de recette dans une colonne"""
    with col:
        with st.container():
            # Afficher l'image de la recette si disponible
            if hasattr(recipe, 'imageUrl') and recipe.imageUrl:
                st.image(recipe.imageUrl, use_container_width=True)
            elif not hasattr(recipe, 'imageUrl'):
                st.info("📷 Image non disponible")
            
            # Titre et bouton favori
            col_title, col_fav = st.columns([4, 1])
            with col_title:
                st.subheader(f"🍽️ {recipe.name}")
            
            with col_fav:
                recipe_id = str(recipe.id) if hasattr(recipe, 'id') else recipe.name
                is_fav = is_favorite(recipe_id)
                fav_button_label = "❤️" if is_fav else "🤍"
                
                if st.button(fav_button_label, key=f"fav_{recipe_id}_{hash(recipe.name)}"):
                    if is_fav:
                        if remove_from_favorites(recipe_id):
                            st.success("Retiré des favoris!")
                            st.rerun()
                    else:
                        prep_time = recipe.preparationTime if hasattr(recipe, 'preparationTime') else None
                        cook_time = recipe.cookingTime if hasattr(recipe, 'cookingTime') else None
                        covers = recipe.coversCount if hasattr(recipe, 'coversCount') else None
                        url = recipe.url if hasattr(recipe, 'url') else ""
                        desc = recipe.description if hasattr(recipe, 'description') else ""
                        ingredients = recipe.ingredients if hasattr(recipe, 'ingredients') else None
                        
                        if save_to_favorites(recipe_id, recipe.name, url, desc, prep_time, cook_time, covers, ingredients):
                            st.success("Ajouté aux favoris!")
                            st.rerun()
            
            # URL de la recette (toujours disponible)
            if hasattr(recipe, 'url') and recipe.url:
                st.markdown(f"🔗 [**Voir sur Jow.fr**]({recipe.url})")
            
            # Description si disponible
            if hasattr(recipe, 'description') and recipe.description:
                st.write(f"📝 {recipe.description}")
            
            # Informations de temps
            col_prep, col_cook = st.columns(2)
            with col_prep:
                if hasattr(recipe, 'preparationTime') and recipe.preparationTime:
                    st.metric("⏱️ Préparation", f"{recipe.preparationTime} min")
            
            with col_cook:
                if hasattr(recipe, 'cookingTime') and recipe.cookingTime:
                    st.metric("🔥 Cuisson", f"{recipe.cookingTime} min")
            
            # Nombre de portions
            if hasattr(recipe, 'coversCount') and recipe.coversCount:
                st.info(f"👥 Pour {recipe.coversCount} personnes")
            
            # Ingrédients si disponibles
            if hasattr(recipe, 'ingredients') and recipe.ingredients:
                with st.expander("📋 Voir les ingrédients"):
                    for ingredient in recipe.ingredients:
                        if hasattr(ingredient, 'name'):
                            quantity_text = ""
                            if hasattr(ingredient, 'quantity') and ingredient.quantity:
                                quantity_text += f"{ingredient.quantity}"
                            if hasattr(ingredient, 'unit') and ingredient.unit:
                                quantity_text += f" {ingredient.unit}"
                            
                            if quantity_text:
                                st.write(f"• {ingredient.name}: {quantity_text}")
                            else:
                                st.write(f"• {ingredient.name}")
            
            # Badge de substitution
            if est_substitution:
                st.success("🔄 Recette adaptée pour ton ingrédient africain !")
            
            st.divider()

def afficher_message_personnalise(query: str, substitution: str):
    """Affiche un message personnalisé pour les substitutions"""
    st.warning(f"🌍 Pas de recette Jow correspondante pour '{query}' ?")
    st.info(f"🔄 Voici des idées inspirées avec **{substitution}** en substitution !")
    st.markdown("### 💡 Astuce culinaire")
    st.write(f"Tu peux facilement remplacer **{substitution}** par **{query}** dans ces recettes pour une touche africaine authentique !")

def afficher_suggestion_fusion():
    """Affiche une suggestion de fusion humoristique"""
    if st.session_state.get('mode_decouverte', True):
        suggestion = SUGGESTIONS_FUSION[hash(str(time.time())) % len(SUGGESTIONS_FUSION)]
        st.success(f"🎭 **Idée Fusion :** {suggestion}")

def filtrer_recettes(recipes, max_prep_time, max_cook_time, serves):
    """Filtre les recettes selon les critères"""
    filtered = []
    for recipe in recipes:
        # Vérifier temps de préparation
        prep_time = recipe.preparationTime if hasattr(recipe, 'preparationTime') and recipe.preparationTime else 0
        cook_time = recipe.cookingTime if hasattr(recipe, 'cookingTime') and recipe.cookingTime else 0
        recipe_serves = recipe.coversCount if hasattr(recipe, 'coversCount') and recipe.coversCount else serves
        
        # Appliquer les filtres
        if prep_time <= max_prep_time and cook_time <= max_cook_time:
            # Pour le nombre de personnes, on accepte une marge de +/- 2
            if abs(recipe_serves - serves) <= 2 or recipe_serves == 0:
                filtered.append(recipe)
    
    return filtered

def afficher_carte_recette_africaine(recipe_data, col):
    """Affiche une carte pour une recette africaine de la BD"""
    with col:
        with st.container():
            # Titre et badge
            st.subheader(f"🌍 {recipe_data[1]}")
            st.success("Recette Traditionnelle Africaine")
            
            # Pays d'origine
            if recipe_data[8]:
                st.write(f"🌍 **Origine:** {recipe_data[8]}")
            
            # Description
            if recipe_data[2]:
                st.write(f"📝 {recipe_data[2]}")
            
            # Informations de temps
            col_prep, col_cook = st.columns(2)
            with col_prep:
                if recipe_data[5]:
                    st.metric("⏱️ Préparation", f"{recipe_data[5]} min")
            
            with col_cook:
                if recipe_data[6]:
                    st.metric("🔥 Cuisson", f"{recipe_data[6]} min")
            
            # Nombre de portions
            if recipe_data[7]:
                st.info(f"👥 Pour {recipe_data[7]} personnes")
            
            # Ingrédients
            if recipe_data[3]:
                with st.expander("📋 Voir les ingrédients"):
                    ingredients = recipe_data[3].split(',')
                    for ing in ingredients:
                        st.write(f"• {ing.strip()}")
            
            # Étapes de préparation
            if recipe_data[4]:
                with st.expander("👨‍🍳 Étapes de préparation"):
                    steps = recipe_data[4].split('.')
                    for idx, step in enumerate(steps):
                        if step.strip():
                            st.write(f"**{idx+1}.** {step.strip()}")
            
            st.divider()

def main():
    """Fonction principale de l'application"""
    # Initialiser la base de données
    if 'db_initialized' not in st.session_state:
        init_database()
        st.session_state.db_initialized = True
    
    # Initialisation des variables de session
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'mode_decouverte' not in st.session_state:
        st.session_state.mode_decouverte = True
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'african_results' not in st.session_state:
        st.session_state.african_results = []
    if 'searched_query_display' not in st.session_state:
        st.session_state.searched_query_display = ""
    if 'is_substitution' not in st.session_state:
        st.session_state.is_substitution = False
    if 'ai_analysis' not in st.session_state:
        st.session_state.ai_analysis = None
    
    # Affichage des éléments principaux
    afficher_titre_principal()
    afficher_sidebar()
    
    # Interface de recherche
    col_search, col_button = st.columns([3, 1])
    
    with col_search:
        query = st.text_input(
            "🔍 Recherche par ingrédient ou mot-clé :",
            value=st.session_state.search_query,
            placeholder="Ex: poulet, tomate, riz, manioc, igname...",
            key="search_input"
        )
    
    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)  # Espacement vertical
        search_clicked = st.button("🔎 Chercher", type="primary", width='stretch')
    
    # Filtres avancés
    with st.expander("🔧 Filtres avancés"):
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            max_prep_time = st.slider("⏱️ Temps de préparation max (min)", 0, 120, 120, 5)
        
        with col_f2:
            max_cook_time = st.slider("🔥 Temps de cuisson max (min)", 0, 120, 120, 5)
        
        with col_f3:
            serves = st.slider("👥 Nombre de personnes", 1, 12, 4)
    
    # Recherche déclenchée
    if search_clicked and query:
        st.session_state.search_query = query
        
        with st.spinner("🤖 Analyse IA en cours..."):
            # Analyser la recherche avec l'IA Gemini
            ai_analysis = enrichir_recherche_avec_ia(query)
            st.session_state.ai_analysis = ai_analysis
        
        with st.spinner("🔍 Recherche de recettes..."):
            # Recherche principale dans Jow
            recipes, searched_query, is_substitution = rechercher_avec_substitution(query)
            
            # Si l'IA suggère d'autres termes et peu de résultats, essayer les suggestions
            if ai_analysis and recipes and len(recipes) < 3 and ai_analysis.get('suggestions_recherche'):
                for suggestion in ai_analysis['suggestions_recherche'][:2]:
                    if suggestion.lower() != query.lower():
                        additional_recipes, _, _ = rechercher_avec_substitution(suggestion)
                        if additional_recipes:
                            recipes = list(recipes) if not isinstance(recipes, list) else recipes
                            recipes.extend(additional_recipes)
            
            # Recherche dans les recettes africaines
            african_recipes = get_african_recipes(query)
            
            # Filtrer les recettes Jow
            if recipes:
                recipes = filtrer_recettes(recipes, max_prep_time, max_cook_time, serves)
            
            # Sauvegarder dans session state
            st.session_state.search_results = recipes
            st.session_state.african_results = african_recipes
            st.session_state.searched_query_display = searched_query
            st.session_state.is_substitution = is_substitution
            
            # Sauvegarder l'historique de recherche
            total_results = len(recipes) + len(african_recipes)
            save_search_history(query, total_results)
            
    
    # Afficher les résultats depuis session state (persiste après favoris)
    if st.session_state.search_results is not None or st.session_state.african_results:
        recipes = st.session_state.search_results if st.session_state.search_results else []
        african_recipes = st.session_state.african_results
        searched_query = st.session_state.searched_query_display
        is_substitution = st.session_state.is_substitution
        ai_analysis = st.session_state.ai_analysis
        
        if recipes or african_recipes:
            # Afficher l'analyse de l'IA
            if ai_analysis:
                if ai_analysis.get('est_africain'):
                    st.success("🌍 🤖 **IA Détectée:** Cette recherche concerne une recette africaine authentique !")
                
                if ai_analysis.get('conseil'):
                    with st.expander("💡 Conseil de l'IA pour africaniser tes recettes"):
                        st.info(ai_analysis['conseil'])
                
                if ai_analysis.get('ingredients_cles'):
                    st.markdown(f"**🌶️ Ingrédients africains clés:** {', '.join(ai_analysis['ingredients_cles'])}")
                
                st.divider()
            
            # Affichage des résultats principaux
            if is_substitution and recipes:
                afficher_message_personnalise(st.session_state.search_query, searched_query)
            
            # Afficher les recettes africaines d'abord si disponibles
            if african_recipes:
                st.markdown(f"### 🌍 Recettes Africaines Traditionnelles ({len(african_recipes)} recettes)")
                cols_per_row = 2
                for i in range(0, len(african_recipes), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, recipe in enumerate(african_recipes[i:i+cols_per_row]):
                        afficher_carte_recette_africaine(recipe, cols[j])
                
                st.divider()
            
            # Puis afficher les recettes Jow
            if recipes:
                st.markdown(f"### 🍽️ Recettes Jow pour '{searched_query}' ({len(recipes)} recettes)")
                
                # Affichage en colonnes
                cols_per_row = 2
                for i in range(0, len(recipes), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, recipe in enumerate(recipes[i:i+cols_per_row]):
                        afficher_carte_recette(recipe, cols[j], is_substitution)
            
            # Suggestion de fusion si mode activé
            afficher_suggestion_fusion()
    
    elif search_clicked and not query:
        st.warning("⚠️ Veuillez saisir un terme de recherche !")
    
    # Message d'accueil si aucune recherche
    elif not st.session_state.search_query:
        st.markdown("### 👋 Bienvenue dans ton assistant culinaire !")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌍 Spécialement conçu pour toi")
            st.write("• Recherche parmi des milliers de recettes Jow.fr")
            st.write("• Suggestions adaptées aux goûts africains")
            st.write("• Substitutions intelligentes d'ingrédients")
            st.write("• Mode fusion Afrique-Europe unique")
        
        with col2:
            st.markdown("#### 🚀 Comment commencer ?")
            st.write("1. Tape un ingrédient dans la barre de recherche")
            st.write("2. Ou clique sur une suggestion dans la barre latérale")
            st.write("3. Active le mode découverte pour des idées fusion")
            st.write("4. Explore et inspire-toi !")
        
        st.success("🎉 Prêt à découvrir de nouvelles saveurs ? Commence ta recherche !")

if __name__ == "__main__":
    main()

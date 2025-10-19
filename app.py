import streamlit as st
from jow_api import Jow
import time
from typing import List, Dict

# Configuration de la page
st.set_page_config(
    page_title="Recettes Jow - Fusion Afrique-Europe",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        st.header("🌍 Recettes Africaines Suggérées")
        st.markdown("Clique pour rechercher ces délices :")
        
        for recette in RECETTES_AFRICAINES_SUGGEREES:
            if st.button(f"🍲 {recette}", key=f"suggestion_{recette}", use_container_width=True):
                st.session_state.search_query = recette
                st.rerun()
        
        st.divider()
        
        # Mode découverte
        st.header("🎭 Mode Découverte")
        mode_decouverte = st.toggle("Activer fusion Afrique-Europe", value=True)
        st.session_state.mode_decouverte = mode_decouverte
        
        if mode_decouverte:
            st.success("Mode fusion activé ! 🎉")
            st.info("Les suggestions de fusion apparaîtront avec tes résultats !")

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
            st.subheader(f"🍽️ {recipe.name}")
            
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

def main():
    """Fonction principale de l'application"""
    # Initialisation des variables de session
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'mode_decouverte' not in st.session_state:
        st.session_state.mode_decouverte = True
    
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
        search_clicked = st.button("🔎 Chercher", type="primary", use_container_width=True)
    
    # Recherche déclenchée
    if search_clicked and query:
        st.session_state.search_query = query
        
        with st.spinner("🔍 Recherche en cours..."):
            # Recherche principale
            recipes, searched_query, is_substitution = rechercher_avec_substitution(query)
            
            if recipes:
                # Affichage des résultats principaux
                if is_substitution:
                    afficher_message_personnalise(query, searched_query)
                
                st.markdown(f"### 🍽️ Résultats pour '{searched_query}' ({len(recipes)} recettes)")
                
                # Affichage en colonnes
                cols_per_row = 2
                for i in range(0, len(recipes), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, recipe in enumerate(recipes[i:i+cols_per_row]):
                        afficher_carte_recette(recipe, cols[j], is_substitution)
                
                # Suggestion de fusion si mode activé
                afficher_suggestion_fusion()
                
            else:
                # Aucune recette trouvée - Tentative de substitution
                recipes_alt, substitution, _ = rechercher_recettes_alternatives(query)
                
                if recipes_alt:
                    afficher_message_personnalise(query, substitution)
                    
                    st.markdown(f"### 🔄 Recettes alternatives avec '{substitution}' ({len(recipes_alt)} recettes)")
                    
                    # Affichage des alternatives
                    cols_per_row = 2
                    for i in range(0, len(recipes_alt), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for j, recipe in enumerate(recipes_alt[i:i+cols_per_row]):
                            afficher_carte_recette(recipe, cols[j], True)
                    
                    afficher_suggestion_fusion()
                    
                else:
                    # Vraiment aucun résultat
                    st.error("😔 Aucune recette trouvée pour cette recherche.")
                    st.info("💡 **Suggestions :**")
                    st.write("• Essaie des mots-clés plus simples (poulet, poisson, riz)")
                    st.write("• Utilise les suggestions dans la barre latérale")
                    st.write("• Vérifie l'orthographe de ta recherche")
                    
                    # Affichage de quelques recettes populaires
                    st.markdown("### 🌟 Recettes populaires à découvrir")
                    cols = st.columns(3)
                    populaires = ["poulet", "pâtes", "salade"]
                    for i, mot in enumerate(populaires):
                        with cols[i]:
                            if st.button(f"Découvrir {mot}", key=f"popular_{mot}"):
                                st.session_state.search_query = mot
                                st.rerun()
    
    elif search_clicked and not query:
        st.warning("⚠️ Veuillez saisir un terme de recherche !")
    
    # Message d'accueil si aucune recherche
    if not st.session_state.search_query:
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

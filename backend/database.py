"""
Gestion de la base de données SQLite
"""
import sqlite3
import os
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
from models import Meal, WeeklyPlan, Statistics, MealType, CuisineType

class DatabaseManager:
    def __init__(self, db_path: str = "jowafrique.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager pour les connexions DB"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialise la base de données avec les tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Table des plans hebdomadaires
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weekly_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plan_name TEXT NOT NULL,
                    week_start_date DATE NOT NULL,
                    total_budget_estimate REAL,
                    generated_by_ai BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des repas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS meal_slots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plan_id INTEGER NOT NULL,
                    day_of_week TEXT NOT NULL,
                    meal_type TEXT NOT NULL,
                    recipe_name TEXT NOT NULL,
                    jow_recipe_id TEXT,
                    jow_recipe_url TEXT,
                    main_ingredient TEXT,
                    cuisine_type TEXT,
                    image_url TEXT,
                    video_url TEXT,
                    prep_time INTEGER,
                    cook_time INTEGER,
                    is_favorite BOOLEAN DEFAULT 0,
                    rating INTEGER DEFAULT 0,
                    notes TEXT,
                    FOREIGN KEY (plan_id) REFERENCES weekly_plans(id)
                )
            """)
            
            # Table des favoris
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jow_recipe_id TEXT NOT NULL,
                    recipe_name TEXT NOT NULL,
                    main_ingredient TEXT,
                    cuisine_type TEXT,
                    image_url TEXT,
                    added_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(jow_recipe_id)
                )
            """)
            
            # Table de l'historique des recettes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipe_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jow_recipe_id TEXT NOT NULL,
                    recipe_name TEXT NOT NULL,
                    main_ingredient TEXT,
                    used_date DATE NOT NULL,
                    plan_id INTEGER,
                    rating INTEGER DEFAULT 0,
                    FOREIGN KEY (plan_id) REFERENCES weekly_plans(id)
                )
            """)
            
            # Table des listes de courses
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shopping_lists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plan_id INTEGER NOT NULL,
                    list_name TEXT NOT NULL,
                    ingredients TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (plan_id) REFERENCES weekly_plans(id)
                )
            """)
            
            # Index pour les performances
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_weekly_plans_date ON weekly_plans(week_start_date DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_meal_slots_plan ON meal_slots(plan_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_meal_slots_favorite ON meal_slots(is_favorite)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipe_history_date ON recipe_history(used_date DESC)")
            
            conn.commit()
    
    def create_plan(self, plan: WeeklyPlan) -> int:
        """Crée un nouveau plan"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO weekly_plans (plan_name, week_start_date, total_budget_estimate, generated_by_ai)
                VALUES (?, ?, ?, ?)
            """, (plan.plan_name, plan.week_start_date, plan.total_budget_estimate, plan.generated_by_ai))
            conn.commit()
            return cursor.lastrowid
    
    def get_plans(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Récupère tous les plans"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, plan_name, week_start_date, total_budget_estimate, 
                       generated_by_ai, created_at
                FROM weekly_plans
                ORDER BY week_start_date DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_plan_meals(self, plan_id: int) -> List[Dict[str, Any]]:
        """Récupère les repas d'un plan"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, day_of_week, meal_type, recipe_name, jow_recipe_id, 
                       jow_recipe_url, main_ingredient, cuisine_type, image_url, 
                       video_url, prep_time, cook_time, is_favorite, rating, notes
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
                    END,
                    CASE meal_type
                        WHEN 'Petit-déjeuner' THEN 1
                        WHEN 'Déjeuner' THEN 2
                        WHEN 'Dîner' THEN 3
                    END
            """, (plan_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def add_meal_to_plan(self, meal: Meal) -> int:
        """Ajoute un repas à un plan"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO meal_slots (plan_id, day_of_week, meal_type, recipe_name, 
                                       jow_recipe_id, jow_recipe_url, main_ingredient, 
                                       cuisine_type, image_url, video_url, prep_time, 
                                       cook_time, is_favorite, rating, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (meal.plan_id, meal.day_of_week, meal.meal_type.value, meal.recipe_name,
                  meal.jow_recipe_id, meal.jow_recipe_url, meal.main_ingredient,
                  meal.cuisine_type.value if meal.cuisine_type else None,
                  meal.image_url, meal.video_url, meal.prep_time, meal.cook_time,
                  meal.is_favorite, meal.rating, meal.notes))
            conn.commit()
            return cursor.lastrowid
    
    def add_base_recipe(self, meal: Meal) -> int:
        """Ajoute une recette de base (sans plan)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO meal_slots (plan_id, day_of_week, meal_type, recipe_name, 
                                       jow_recipe_id, jow_recipe_url, main_ingredient, 
                                       cuisine_type, image_url, video_url, prep_time, 
                                       cook_time, is_favorite, rating, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (None, None, meal.meal_type.value, meal.recipe_name,
                  meal.jow_recipe_id, meal.jow_recipe_url, meal.main_ingredient,
                  meal.cuisine_type.value if meal.cuisine_type else None,
                  meal.image_url, meal.video_url, meal.prep_time, meal.cook_time,
                  meal.is_favorite, meal.rating, meal.notes))
            conn.commit()
            return cursor.lastrowid
    
    def update_meal(self, meal_id: int, updates: Dict[str, Any]) -> bool:
        """Met à jour un repas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            set_clauses = []
            values = []
            
            for key, value in updates.items():
                if key in ['is_favorite', 'rating', 'notes']:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)
            
            if set_clauses:
                values.append(meal_id)
                query = f"UPDATE meal_slots SET {', '.join(set_clauses)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
            return False
    
    def get_statistics(self) -> Statistics:
        """Récupère les statistiques"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total plans
            cursor.execute("SELECT COUNT(*) FROM weekly_plans")
            total_plans = cursor.fetchone()[0]
            
            # Total recipes
            cursor.execute("SELECT COUNT(*) FROM meal_slots")
            total_recipes = cursor.fetchone()[0]
            
            # Favorite recipes
            cursor.execute("SELECT COUNT(*) FROM meal_slots WHERE is_favorite = 1")
            favorite_recipes = cursor.fetchone()[0]
            
            # Average rating
            cursor.execute("SELECT AVG(rating) FROM meal_slots WHERE rating > 0")
            avg_rating = cursor.fetchone()[0] or 0
            
            # Top ingredients
            cursor.execute("""
                SELECT main_ingredient, COUNT(*) as count
                FROM meal_slots
                WHERE main_ingredient IS NOT NULL
                GROUP BY main_ingredient
                ORDER BY count DESC
                LIMIT 5
            """)
            top_ingredients = [(row[0], row[1]) for row in cursor.fetchall()]
            
            return Statistics(
                total_plans=total_plans,
                total_recipes=total_recipes,
                favorite_recipes=favorite_recipes,
                avg_rating=round(avg_rating, 1),
                top_ingredients=top_ingredients
            )
    
    def delete_plan(self, plan_id: int) -> bool:
        """Supprime un plan et ses repas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM meal_slots WHERE plan_id = ?", (plan_id,))
            cursor.execute("DELETE FROM weekly_plans WHERE id = ?", (plan_id,))
            conn.commit()
            return cursor.rowcount > 0

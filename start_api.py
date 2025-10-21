#!/usr/bin/env python3
"""
Script de démarrage pour l'API JowAfrique
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import flask
        import flask_cors
        print("✅ Flask et Flask-CORS installés")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("Installez avec: pip install flask flask-cors")
        return False
    
    return True

def check_database():
    """Vérifie que la base de données existe"""
    print("🔍 Vérification de la base de données...")
    
    db_path = Path("backend/jowafrique.db")
    if db_path.exists():
        print("✅ Base de données trouvée")
        return True
    else:
        print("⚠️  Base de données non trouvée, elle sera créée automatiquement")
        return True

def start_api():
    """Démarre l'API"""
    print("🚀 Démarrage de l'API JowAfrique...")
    
    # Changer vers le répertoire backend
    os.chdir("backend")
    
    try:
        # Démarrer l'API
        subprocess.run([sys.executable, "api.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'API")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return False
    
    return True

def test_api():
    """Teste que l'API répond"""
    print("🧪 Test de l'API...")
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API opérationnelle")
            return True
        else:
            print(f"❌ API répond avec le code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 50)
    print("🍽️  JowAfrique API Starter")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_dependencies():
        sys.exit(1)
    
    if not check_database():
        sys.exit(1)
    
    print("\n📋 Informations de l'API:")
    print("   URL: http://localhost:5000")
    print("   Health Check: http://localhost:5000/api/health")
    print("   Documentation: http://localhost:5000/api/")
    print("\n💡 Appuyez sur Ctrl+C pour arrêter l'API")
    print("=" * 50)
    
    # Démarrer l'API
    start_api()

if __name__ == "__main__":
    main()

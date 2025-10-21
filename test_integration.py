#!/usr/bin/env python3
"""
Script de test simple pour vérifier l'intégration
"""

import requests
import json
import time
import sys

def test_backend_health():
    """Teste si le backend est accessible"""
    try:
        response = requests.get('http://localhost:5000/api/meals', timeout=5)
        if response.status_code == 200:
            print("OK - Backend accessible sur http://localhost:5000")
            return True
        else:
            print(f"ERREUR - Backend repond avec le code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("ERREUR - Impossible de se connecter au backend sur http://localhost:5000")
        print("   Assurez-vous que le backend est demarre avec: python backend/api.py")
        return False
    except Exception as e:
        print(f"ERREUR - Erreur lors du test du backend: {e}")
        return False

def test_endpoints():
    """Teste les endpoints principaux"""
    endpoints = [
        ('/api/meals', 'GET'),
        ('/api/current-meal', 'GET'),
        ('/api/plans', 'GET'),
        ('/api/favorites', 'GET'),
        ('/api/statistics', 'GET'),
    ]
    
    print("\nTest des endpoints...")
    
    for endpoint, method in endpoints:
        try:
            url = f'http://localhost:5000{endpoint}'
            if method == 'GET':
                response = requests.get(url, timeout=5)
            elif method == 'POST':
                response = requests.post(url, json={}, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"OK - {method} {endpoint} - {len(data) if isinstance(data, list) else 'OK'}")
            else:
                print(f"ATTENTION - {method} {endpoint} - Code {response.status_code}")
                
        except Exception as e:
            print(f"ERREUR - {method} {endpoint} - Erreur: {e}")

def test_frontend_health():
    """Teste si le frontend est accessible"""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("OK - Frontend accessible sur http://localhost:3000")
            return True
        else:
            print(f"ERREUR - Frontend repond avec le code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("ERREUR - Impossible de se connecter au frontend sur http://localhost:3000")
        print("   Assurez-vous que le frontend est demarre avec: cd frontend && npm run dev")
        return False
    except Exception as e:
        print(f"ERREUR - Erreur lors du test du frontend: {e}")
        return False

def main():
    print("Test d'integration Frontend-Backend JowAfrique")
    print("=" * 50)
    
    # Test du backend
    backend_ok = test_backend_health()
    
    if backend_ok:
        test_endpoints()
    
    # Test du frontend
    frontend_ok = test_frontend_health()
    
    print("\n" + "=" * 50)
    if backend_ok and frontend_ok:
        print("SUCCES - Integration complete fonctionnelle!")
        print("   Backend: http://localhost:5000")
        print("   Frontend: http://localhost:3000")
    elif backend_ok:
        print("ATTENTION - Backend OK, Frontend non accessible")
        print("   Demarrez le frontend avec: cd frontend && npm run dev")
    elif frontend_ok:
        print("ATTENTION - Frontend OK, Backend non accessible")
        print("   Demarrez le backend avec: python backend/api.py")
    else:
        print("ERREUR - Aucun service accessible")
        print("   Demarrez les services avec: python start.py")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script de test simple pour l'API JowAfrique
"""

import requests
import json
import time
import sys
from datetime import datetime

API_BASE = "http://localhost:5000/api"

def test_health():
    """Test du health check"""
    print("Test du health check...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"OK - Health check - Status: {data['status']}, Version: {data['version']}")
            return True
        else:
            print(f"ERREUR - Health check echoue - Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERREUR - Health check: {e}")
        return False

def test_plans():
    """Test des endpoints plans"""
    print("\nTest des endpoints plans...")
    
    # Test GET /plans
    try:
        response = requests.get(f"{API_BASE}/plans", timeout=5)
        if response.status_code == 200:
            plans = response.json()
            print(f"OK - GET /plans - {len(plans)} plans trouves")
        else:
            print(f"ERREUR - GET /plans echoue - Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERREUR - GET /plans: {e}")
        return False
    
    return True

def test_statistics():
    """Test des endpoints statistiques"""
    print("\nTest des endpoints statistiques...")
    
    try:
        response = requests.get(f"{API_BASE}/statistics", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"OK - GET /statistics - {stats}")
            return True
        else:
            print(f"ERREUR - GET /statistics echoue - Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERREUR - GET /statistics: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("Test de l'API JowAfrique")
    print("=" * 60)
    
    # Vérifier que l'API est accessible
    print("Verification de l'accessibilite de l'API...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code != 200:
            print("ERREUR: API non accessible. Demarrez l'API avec: python backend/api.py")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("ERREUR: API non accessible. Demarrez l'API avec: python backend/api.py")
        sys.exit(1)
    
    # Tests
    tests = [
        test_health,
        test_plans,
        test_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)
    
    # Résultats
    print("\n" + "=" * 60)
    print(f"Resultats: {passed}/{total} tests reussis")
    
    if passed == total:
        print("SUCCES: Tous les tests sont passes avec succes!")
        print("L'API JowAfrique fonctionne correctement")
    else:
        print("ATTENTION: Certains tests ont echoue")
        print("Verifiez les logs de l'API pour plus de details")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

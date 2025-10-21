#!/usr/bin/env python3
"""
Script de démarrage simple pour JowAfrique
Lance le backend Flask et le frontend Next.js
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def start_backend():
    """Démarre le backend Flask"""
    print("🚀 Démarrage du backend Flask...")
    backend_dir = Path(__file__).parent / "backend"
    
    # Installer les dépendances si nécessaire
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements_api.txt"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass  # Ignorer les erreurs d'installation
    
    # Démarrer le backend
    return subprocess.Popen([
        sys.executable, "api.py"
    ], cwd=backend_dir)

def start_frontend():
    """Démarre le frontend Next.js"""
    print("📱 Démarrage du frontend Next.js...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Installer les dépendances si nécessaire
    try:
        subprocess.check_call([
            "npm", "install"
        ], cwd=frontend_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass  # Ignorer les erreurs d'installation
    
    # Démarrer le frontend
    return subprocess.Popen([
        "npm", "run", "dev"
    ], cwd=frontend_dir)

def main():
    print("🌟 JowAfrique - Démarrage de l'application")
    print("=" * 50)
    
    try:
        # Démarrer le backend
        backend_process = start_backend()
        time.sleep(3)  # Attendre que le backend démarre
        
        # Démarrer le frontend
        frontend_process = start_frontend()
        
        print("\n✅ Services démarrés:")
        print("   Backend API: http://localhost:5000")
        print("   Frontend: http://localhost:3000")
        print("\nAppuyez sur Ctrl+C pour arrêter les services")
        
        # Attendre que les processus se terminent
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("❌ Backend arrêté")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend arrêté")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des services...")
        
        # Arrêter les processus
        if 'backend_process' in locals():
            backend_process.terminate()
        if 'frontend_process' in locals():
            frontend_process.terminate()
        
        print("✅ Services arrêtés")

if __name__ == "__main__":
    main()

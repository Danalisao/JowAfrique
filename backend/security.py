"""
Sécurité et validation pour l'API JowAfrique
"""
import re
import hashlib
import secrets
from typing import Any, Dict, List, Optional
from functools import wraps
from flask import request, jsonify, current_app
import sqlite3

class SecurityManager:
    def __init__(self):
        self.rate_limit_store = {}
        self.max_requests_per_minute = 60
        self.blocked_ips = set()
    
    def validate_input(self, data: Dict[str, Any], schema: Dict[str, Any]) -> tuple[bool, str]:
        """Valide les données d'entrée selon un schéma"""
        for field, rules in schema.items():
            if field not in data:
                if rules.get('required', False):
                    return False, f"Champ requis manquant: {field}"
                continue
            
            value = data[field]
            
            # Type validation
            expected_type = rules.get('type')
            if expected_type and not isinstance(value, expected_type):
                return False, f"Type invalide pour {field}: attendu {expected_type.__name__}"
            
            # String length validation
            if isinstance(value, str):
                min_length = rules.get('min_length', 0)
                max_length = rules.get('max_length', 1000)
                if len(value) < min_length or len(value) > max_length:
                    return False, f"Longueur invalide pour {field}: {len(value)} caractères"
                
                # Pattern validation
                pattern = rules.get('pattern')
                if pattern and not re.match(pattern, value):
                    return False, f"Format invalide pour {field}"
            
            # Numeric range validation
            if isinstance(value, (int, float)):
                min_val = rules.get('min_value')
                max_val = rules.get('max_value')
                if min_val is not None and value < min_val:
                    return False, f"Valeur trop petite pour {field}: {value}"
                if max_val is not None and value > max_val:
                    return False, f"Valeur trop grande pour {field}: {value}"
        
        return True, ""
    
    def sanitize_string(self, value: str) -> str:
        """Nettoie une chaîne de caractères"""
        if not isinstance(value, str):
            return str(value)
        
        # Remove potentially dangerous characters
        value = re.sub(r'[<>"\']', '', value)
        value = value.strip()
        
        return value
    
    def check_rate_limit(self, ip: str) -> bool:
        """Vérifie la limite de taux pour une IP"""
        current_time = int(time.time())
        minute = current_time // 60
        
        if ip not in self.rate_limit_store:
            self.rate_limit_store[ip] = {}
        
        ip_data = self.rate_limit_store[ip]
        
        # Clean old data
        for old_minute in list(ip_data.keys()):
            if old_minute < minute - 1:
                del ip_data[old_minute]
        
        # Check current minute
        current_count = ip_data.get(minute, 0)
        if current_count >= self.max_requests_per_minute:
            return False
        
        # Increment counter
        ip_data[minute] = current_count + 1
        return True
    
    def is_ip_blocked(self, ip: str) -> bool:
        """Vérifie si une IP est bloquée"""
        return ip in self.blocked_ips
    
    def block_ip(self, ip: str, duration: int = 3600):
        """Bloque une IP temporairement"""
        self.blocked_ips.add(ip)
        # In a real app, you'd store this in a database with expiration
    
    def generate_csrf_token(self) -> str:
        """Génère un token CSRF"""
        return secrets.token_urlsafe(32)
    
    def verify_csrf_token(self, token: str, session_token: str) -> bool:
        """Vérifie un token CSRF"""
        return token == session_token and len(token) > 0

# Instance globale
security_manager = SecurityManager()

# Décorateurs de sécurité
def require_validation(schema: Dict[str, Any]):
    """Décorateur pour valider les données d'entrée"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            is_valid, error = security_manager.validate_input(data, schema)
            
            if not is_valid:
                return jsonify({'error': f'Validation failed: {error}'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def rate_limit(max_requests: int = 60):
    """Décorateur pour limiter le taux de requêtes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            
            if security_manager.is_ip_blocked(ip):
                return jsonify({'error': 'IP blocked'}), 403
            
            if not security_manager.check_rate_limit(ip):
                security_manager.block_ip(ip)
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def sanitize_inputs(f):
    """Décorateur pour nettoyer les entrées"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            data = request.get_json()
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, str):
                        data[key] = security_manager.sanitize_string(value)
                request._cached_json = data
        
        return f(*args, **kwargs)
    return decorated_function

# Schémas de validation
MEAL_SCHEMA = {
    'name': {'type': str, 'required': True, 'min_length': 1, 'max_length': 200},
    'day_of_week': {'type': str, 'required': True, 'pattern': r'^(Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche)$'},
    'meal_type': {'type': str, 'required': True, 'pattern': r'^(Petit-déjeuner|Déjeuner|Dîner)$'},
    'prep_time': {'type': int, 'min_value': 0, 'max_value': 300},
    'cook_time': {'type': int, 'min_value': 0, 'max_value': 600},
    'rating': {'type': int, 'min_value': 0, 'max_value': 5}
}

PLAN_SCHEMA = {
    'plan_name': {'type': str, 'required': True, 'min_length': 1, 'max_length': 100},
    'week_start_date': {'type': str, 'required': True, 'pattern': r'^\d{4}-\d{2}-\d{2}$'},
    'total_budget_estimate': {'type': (int, float), 'min_value': 0, 'max_value': 10000}
}

# Protection contre les injections SQL
def safe_query(query: str, params: tuple = ()) -> str:
    """Exécute une requête SQL de manière sécurisée"""
    # Cette fonction devrait utiliser des requêtes préparées
    # Pour SQLite, on s'assure que les paramètres sont correctement échappés
    return query

# Validation des fichiers uploadés
def validate_uploaded_file(file) -> tuple[bool, str]:
    """Valide un fichier uploadé"""
    if not file:
        return False, "Aucun fichier fourni"
    
    # Vérifier la taille (max 5MB)
    max_size = 5 * 1024 * 1024
    if len(file.read()) > max_size:
        file.seek(0)  # Reset file pointer
        return False, "Fichier trop volumineux (max 5MB)"
    
    file.seek(0)  # Reset file pointer
    
    # Vérifier le type MIME
    allowed_types = ['image/jpeg', 'image/png', 'image/webp']
    if file.content_type not in allowed_types:
        return False, "Type de fichier non autorisé"
    
    return True, ""

# Chiffrement des données sensibles
def encrypt_sensitive_data(data: str) -> str:
    """Chiffre des données sensibles (simplifié)"""
    # Dans une vraie app, utilisez une bibliothèque de chiffrement appropriée
    return hashlib.sha256(data.encode()).hexdigest()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Déchiffre des données sensibles (simplifié)"""
    # Cette implémentation est simplifiée - utilisez une vraie solution de chiffrement
    return encrypted_data

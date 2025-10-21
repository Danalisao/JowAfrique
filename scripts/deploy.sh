#!/bin/bash

# Script de déploiement pour JowAfrique
set -e

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
VERSION=${2:-latest}
REGISTRY=${3:-your-registry.com}
PROJECT_NAME="jowafrique"

echo -e "${BLUE}🚀 Déploiement de JowAfrique v${VERSION} en ${ENVIRONMENT}${NC}"

# Fonction de logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

# Vérifier les prérequis
check_prerequisites() {
    log "Vérification des prérequis..."
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        error "Docker n'est pas installé"
    fi
    
    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose n'est pas installé"
    fi
    
    # Vérifier les variables d'environnement
    if [ ! -f ".env.${ENVIRONMENT}" ]; then
        error "Fichier .env.${ENVIRONMENT} manquant"
    fi
    
    log "Prérequis validés ✅"
}

# Construire les images
build_images() {
    log "Construction des images Docker..."
    
    # Backend
    log "Construction de l'image backend..."
    docker build -t ${REGISTRY}/${PROJECT_NAME}-backend:${VERSION} ./backend
    docker tag ${REGISTRY}/${PROJECT_NAME}-backend:${VERSION} ${REGISTRY}/${PROJECT_NAME}-backend:latest
    
    # Frontend
    log "Construction de l'image frontend..."
    docker build -t ${REGISTRY}/${PROJECT_NAME}-frontend:${VERSION} ./frontend
    docker tag ${REGISTRY}/${PROJECT_NAME}-frontend:${VERSION} ${REGISTRY}/${PROJECT_NAME}-frontend:latest
    
    log "Images construites ✅"
}

# Pousser les images vers le registry
push_images() {
    log "Poussée des images vers le registry..."
    
    docker push ${REGISTRY}/${PROJECT_NAME}-backend:${VERSION}
    docker push ${REGISTRY}/${PROJECT_NAME}-backend:latest
    docker push ${REGISTRY}/${PROJECT_NAME}-frontend:${VERSION}
    docker push ${REGISTRY}/${PROJECT_NAME}-frontend:latest
    
    log "Images poussées ✅"
}

# Déployer avec Docker Compose
deploy() {
    log "Déploiement avec Docker Compose..."
    
    # Charger les variables d'environnement
    export $(cat .env.${ENVIRONMENT} | xargs)
    
    # Arrêter les services existants
    docker-compose -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml down
    
    # Démarrer les nouveaux services
    docker-compose -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml up -d
    
    log "Déploiement terminé ✅"
}

# Vérifier la santé des services
health_check() {
    log "Vérification de la santé des services..."
    
    # Attendre que les services soient prêts
    sleep 30
    
    # Vérifier le backend
    if curl -f http://localhost:5000/api/v2/health > /dev/null 2>&1; then
        log "Backend: ✅"
    else
        error "Backend: ❌ Service non disponible"
    fi
    
    # Vérifier le frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log "Frontend: ✅"
    else
        error "Frontend: ❌ Service non disponible"
    fi
    
    # Vérifier la base de données
    if docker-compose exec -T postgres pg_isready -U jowafrique > /dev/null 2>&1; then
        log "Base de données: ✅"
    else
        error "Base de données: ❌ Service non disponible"
    fi
    
    log "Tous les services sont opérationnels ✅"
}

# Nettoyer les images inutilisées
cleanup() {
    log "Nettoyage des images inutilisées..."
    
    # Supprimer les images dangling
    docker image prune -f
    
    # Supprimer les images non utilisées
    docker image prune -a -f
    
    log "Nettoyage terminé ✅"
}

# Rollback en cas d'erreur
rollback() {
    error "Erreur détectée, rollback en cours..."
    
    # Restaurer la version précédente
    docker-compose -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml down
    docker-compose -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml up -d
    
    error "Rollback terminé"
}

# Fonction principale
main() {
    # Gérer les signaux d'arrêt
    trap rollback ERR
    
    check_prerequisites
    build_images
    
    if [ "$ENVIRONMENT" != "local" ]; then
        push_images
    fi
    
    deploy
    health_check
    cleanup
    
    log "🎉 Déploiement réussi!"
    log "Frontend: http://localhost:3000"
    log "Backend: http://localhost:5000"
    log "Grafana: http://localhost:3001"
    log "Prometheus: http://localhost:9090"
}

# Exécuter le script
main "$@"

#!/bin/bash

# Script de sauvegarde pour JowAfrique
set -e

# Configuration
BACKUP_DIR="/backups/jowafrique"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Couleurs pour les logs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

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

# Créer le répertoire de sauvegarde
create_backup_dir() {
    log "Création du répertoire de sauvegarde..."
    mkdir -p "${BACKUP_DIR}/${DATE}"
}

# Sauvegarder la base de données PostgreSQL
backup_database() {
    log "Sauvegarde de la base de données PostgreSQL..."
    
    # Créer un dump de la base de données
    docker-compose exec -T postgres pg_dump -U jowafrique jowafrique > "${BACKUP_DIR}/${DATE}/database.sql"
    
    # Compresser le dump
    gzip "${BACKUP_DIR}/${DATE}/database.sql"
    
    log "Base de données sauvegardée ✅"
}

# Sauvegarder les fichiers de configuration
backup_configs() {
    log "Sauvegarde des fichiers de configuration..."
    
    # Créer un archive des configurations
    tar -czf "${BACKUP_DIR}/${DATE}/configs.tar.gz" \
        docker-compose.yml \
        nginx/ \
        monitoring/ \
        scripts/ \
        .env.* 2>/dev/null || true
    
    log "Configurations sauvegardées ✅"
}

# Sauvegarder les logs
backup_logs() {
    log "Sauvegarde des logs..."
    
    # Créer un archive des logs
    tar -czf "${BACKUP_DIR}/${DATE}/logs.tar.gz" \
        -C /var/lib/docker/volumes logs/ 2>/dev/null || true
    
    log "Logs sauvegardées ✅"
}

# Sauvegarder les uploads
backup_uploads() {
    log "Sauvegarde des fichiers uploadés..."
    
    # Créer un archive des uploads
    tar -czf "${BACKUP_DIR}/${DATE}/uploads.tar.gz" \
        -C /var/lib/docker/volumes uploads/ 2>/dev/null || true
    
    log "Uploads sauvegardés ✅"
}

# Créer un manifest de sauvegarde
create_manifest() {
    log "Création du manifest de sauvegarde..."
    
    cat > "${BACKUP_DIR}/${DATE}/manifest.json" << EOF
{
    "backup_date": "$(date -Iseconds)",
    "version": "$(git describe --tags --always 2>/dev/null || echo 'unknown')",
    "environment": "$(hostname)",
    "files": [
        "database.sql.gz",
        "configs.tar.gz",
        "logs.tar.gz",
        "uploads.tar.gz"
    ],
    "size": "$(du -sh ${BACKUP_DIR}/${DATE} | cut -f1)"
}
EOF
    
    log "Manifest créé ✅"
}

# Nettoyer les anciennes sauvegardes
cleanup_old_backups() {
    log "Nettoyage des anciennes sauvegardes..."
    
    # Supprimer les sauvegardes plus anciennes que RETENTION_DAYS
    find "${BACKUP_DIR}" -type d -mtime +${RETENTION_DAYS} -exec rm -rf {} \; 2>/dev/null || true
    
    log "Nettoyage terminé ✅"
}

# Vérifier l'intégrité de la sauvegarde
verify_backup() {
    log "Vérification de l'intégrité de la sauvegarde..."
    
    # Vérifier que tous les fichiers existent
    local files=("database.sql.gz" "configs.tar.gz" "logs.tar.gz" "uploads.tar.gz" "manifest.json")
    
    for file in "${files[@]}"; do
        if [ ! -f "${BACKUP_DIR}/${DATE}/${file}" ]; then
            warn "Fichier manquant: ${file}"
        fi
    done
    
    # Vérifier la taille de la sauvegarde
    local size=$(du -sm "${BACKUP_DIR}/${DATE}" | cut -f1)
    if [ "$size" -lt 1 ]; then
        error "Sauvegarde trop petite: ${size}MB"
    fi
    
    log "Vérification terminée ✅"
}

# Envoyer une notification (optionnel)
send_notification() {
    local status=$1
    local message="Sauvegarde JowAfrique ${status}: ${DATE}"
    
    # Ici vous pouvez ajouter l'envoi d'email, Slack, etc.
    log "Notification: ${message}"
}

# Fonction de restauration
restore() {
    local backup_date=$1
    
    if [ -z "$backup_date" ]; then
        error "Date de sauvegarde requise pour la restauration"
    fi
    
    log "Restauration depuis la sauvegarde du ${backup_date}..."
    
    # Arrêter les services
    docker-compose down
    
    # Restaurer la base de données
    if [ -f "${BACKUP_DIR}/${backup_date}/database.sql.gz" ]; then
        log "Restauration de la base de données..."
        gunzip -c "${BACKUP_DIR}/${backup_date}/database.sql.gz" | \
        docker-compose exec -T postgres psql -U jowafrique jowafrique
    fi
    
    # Redémarrer les services
    docker-compose up -d
    
    log "Restauration terminée ✅"
}

# Fonction principale
main() {
    case "${1:-backup}" in
        "backup")
            log "Début de la sauvegarde JowAfrique..."
            create_backup_dir
            backup_database
            backup_configs
            backup_logs
            backup_uploads
            create_manifest
            verify_backup
            cleanup_old_backups
            send_notification "SUCCÈS"
            log "Sauvegarde terminée avec succès ✅"
            ;;
        "restore")
            restore "$2"
            ;;
        "list")
            log "Liste des sauvegardes disponibles:"
            ls -la "${BACKUP_DIR}" | grep "^d" | awk '{print $9}' | grep -E '^[0-9]{8}_[0-9]{6}$'
            ;;
        *)
            echo "Usage: $0 {backup|restore <date>|list}"
            echo "  backup  - Créer une nouvelle sauvegarde"
            echo "  restore - Restaurer depuis une sauvegarde"
            echo "  list    - Lister les sauvegardes disponibles"
            exit 1
            ;;
    esac
}

# Exécuter le script
main "$@"

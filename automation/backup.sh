#!/bin/bash

#############################################################################
# Campus IT Helpdesk - Backup & Disaster Recovery Script
# Student ID: 25RP19452-NIYONKURU
# Purpose: Automated backup of database and application data
#############################################################################

set -e

# Configuration
PROJECT_ID="25RP19452-NIYONKURU"
BACKUP_DIR="/home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/backups"
CONTAINER_NAME="25RP19452-NIYONKURU-helpdesk"
DATA_PATH="/data"
RETENTION_DAYS=7

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Function to backup database
backup_database() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Starting database backup..."
    
    BACKUP_FILE="${BACKUP_DIR}/tickets-$(date +'%Y%m%d_%H%M%S').db"
    
    # Copy database from running container
    docker cp "${CONTAINER_NAME}:${DATA_PATH}/tickets.db" "$BACKUP_FILE" 2>/dev/null || {
        echo "Error: Could not backup database"
        return 1
    }
    
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Database backed up to: $BACKUP_FILE"
    ls -lh "$BACKUP_FILE"
}

# Function to backup application logs
backup_logs() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Starting logs backup..."
    
    LOG_BACKUP="${BACKUP_DIR}/logs-$(date +'%Y%m%d_%H%M%S').tar.gz"
    
    docker exec "${CONTAINER_NAME}" tar czf - /var/log/helpdesk 2>/dev/null | \
        cat > "$LOG_BACKUP" || {
        echo "Error: Could not backup logs"
        return 1
    }
    
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Logs backed up to: $LOG_BACKUP"
    ls -lh "$LOG_BACKUP"
}

# Function to cleanup old backups
cleanup_old_backups() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Cleaning up old backups (older than ${RETENTION_DAYS} days)..."
    
    find "$BACKUP_DIR" -type f -mtime +${RETENTION_DAYS} -delete
    
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Cleanup completed"
}

# Function to restore database
restore_database() {
    local backup_file=$1
    
    if [ ! -f "$backup_file" ]; then
        echo "Error: Backup file not found: $backup_file"
        return 1
    fi
    
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Restoring database from: $backup_file"
    
    # Stop the container
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    
    # Copy backup to container
    docker cp "$backup_file" "${CONTAINER_NAME}:${DATA_PATH}/tickets.db"
    
    # Start the container
    docker start "$CONTAINER_NAME"
    
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Database restore completed"
}

# Main execution
echo "========================================"
echo "Backup Script - ${PROJECT_ID}"
echo "========================================"

backup_database
backup_logs
cleanup_old_backups

echo "========================================"
echo "Backup completed successfully"
echo "========================================"

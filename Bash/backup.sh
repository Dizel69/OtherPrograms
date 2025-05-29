#!/bin/bash
SRC_DIR="/home/user/database"
DEST_DIR="/home/user/backup"
DATE_TAG="$(date '+%Y%m%d')"

mkdir -p "$DEST_DIR"
tar czf "${DEST_DIR}/database_backup_${DATE_TAG}.tar.gz" -C "$SRC_DIR" .
#!/bin/bash

# Название скрипта
SCRIPT_NAME=$(basename "$0")

# Директория для логов
LOG_DIR="/var/log/backup"
LOG_FILE="$LOG_DIR/backup.log"

# Директория для бэкапов
BACKUP_DIR="/var/backups/postgres"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_FILE="$BACKUP_DIR/pg_backup_$TIMESTAMP.sql"

# Параметры подключения к PostgreSQL
DB_NAME="your_database_name"
DB_USER="your_database_user"
DB_PASSWORD="your_database_password"

# Убедиться, что директории существуют
mkdir -p "$LOG_DIR"
mkdir -p "$BACKUP_DIR"

# Функция для записи логов
log() {
    echo "[$SCRIPT_NAME][$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "$LOG_FILE"
}

# Начало бэкапа
log "Начало бэкапа базы данных $DB_NAME"

# Экспортировать пароль для pg_dump
export PGPASSWORD="$DB_PASSWORD"

# Выполнение pg_dump и запись вывода в лог
pg_dump -U "$DB_USER" -F c -b -v -f "$BACKUP_FILE" "$DB_NAME" 2>&1 | tee -a "$LOG_FILE"

# Проверка успешности выполнения pg_dump
if [ "${PIPESTATUS[0]}" -eq 0 ]; then
    log "Бэкап базы данных $DB_NAME успешно завершен. Файл: $BACKUP_FILE"
else
    log "Ошибка при создании бэкапа базы данных $DB_NAME"
fi

# Удаление переменной окружения пароля
unset PGPASSWORD

log "Завершение выполнения скрипта"
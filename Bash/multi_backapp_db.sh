#!/bin/bash

# === Настройки ===

# Список баз для бэкапа (можно вписывать любое количество)
DATABASES=("first_db" "second_db" "third_db" "" "medo_isbu")

# Пользователь PostgreSQL
DB_USER="postgres"
export PGPASSWORD="postgres"

# Хост и порт
DB_HOST="196.165.123.45"
DB_PORT="5432"

# Дата
DATE_STR=$(date +'%Y%m%d')

# Каталоги
BACKUP_DIR="/home/backups/postgresql/$DATE_STR"
LOG_DIR="/home/backups/logs"
LOG_FILE="$LOG_DIR/backup_$DATE_STR.log"

# Кол-во дней для хранения
RETENTION_DAYS=3

# === Подготовка ===

mkdir -p "$BACKUP_DIR" "$LOG_DIR"
if [ $? -ne 0 ]; then
  echo "☠️ ERROR: Не удалось создать каталоги:"
  echo "    $BACKUP_DIR"
  echo "    $LOG_DIR"
  exit 1
fi

echo "🕓 $(date +'%F %T') Начинаем backup баз данных..." | tee -a "$LOG_FILE"

# === Бэкап каждой базы ===

for DB_NAME in "${DATABASES[@]}"; do
  BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE_STR}.sql.gz"
  echo "----> Бэкап базы: $DB_NAME" | tee -a "$LOG_FILE"
  
  pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE" 2>> "$LOG_FILE"
  
  if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "💾 $(date +'%F %T') Backup сохранён в $BACKUP_FILE" | tee -a "$LOG_FILE"
  else
    echo "☠️ ERROR: pg_dump провалился. Смотри детали в $LOG_FILE" | tee -a "$LOG_FILE"
  fi
done

# === Удаление старых бэкапов ===

echo "🧹 $(date +'%F %T') Удаляем папки с бэкапами старше $RETENTION_DAYS дней..." | tee -a "$LOG_FILE"
find "/home/backups/postgresql" -maxdepth 1 -mindepth 1 -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \; -print >> "$LOG_FILE" 2>&1
echo "✅ Очистка завершена." | tee -a "$LOG_FILE"

echo "❤️ $(date +'%F %T') Backup скрипт завершён успешно. Лог: $LOG_FILE" | tee -a "$LOG_FILE"

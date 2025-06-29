#!/bin/bash

# =======================#
#  Настройки скрипта     #
# =======================#

# Имя базы данных
DB_NAME="t352"

# Пользователь PostgreSQL, у которого есть права на дамп
DB_USER="postgres"

# Хост и порт PostgreSQL
DB_HOST="10.0.11.128"
DB_PORT="5432"

# Пароль для DB_USER 
export PGPASSWORD="postgres"

# Каталог для хранения бэкапов
BACKUP_DIR="/home/usr/backups/postgresql"

# Файл логов
LOG_FILE="/home/usr/backups/logs/backup.log"

# Директория логов
LOG_DIR="/home/usr/backups/logs"

# Сколько дней хранить резервные копии
RETENTION_DAYS=3

# =======================#
#   Начало выполнения    #
# =======================#

# Проверим, что скрипт запущен с правами суперпользователя
if [ "$(id -u)" -ne 0 ]; then
  echo "☠️ ERROR: Скрипт должен быть запущен от root." | tee -a "$LOG_FILE"
  exit 1
fi

mkdir -p "$BACKUP_DIR" "$LOG_DIR"
if [ $? -ne 0 ]; then
  echo "☠️ ERROR: Не удалось создать каталоги:"
  echo "    $BACKUP_DIR"
  echo "    $LOG_DIR"
  exit 1
fi

# Имя файла для бэкапа с текущей датой
DATE_STR=$(date +'%Y%m%d')
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE_STR}.sql.gz"

echo "🕓 $(date +'%F %T') Начинаем backup базы данных '$DB_NAME'..." | tee -a "$LOG_FILE"

# Выполняем дамп и сразу же сжимаем
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE" 2>> "$LOG_FILE"
if [ ${PIPESTATUS[0]} -ne 0 ]; then
  echo "☠️ ERROR: pg_dump провалился. Смотри детали в $LOG_FILE" | tee -a "$LOG_FILE"
  exit 1
fi

echo "💾 $(date +'%F %T') Backup сохранён в $BACKUP_FILE" | tee -a "$LOG_FILE"

# Удаляем старые бэкапы
echo "🔧 $(date +'%F %T') Удаляем backups старше чем ${RETENTION_DAYS} дня..." | tee -a "$LOG_FILE"
find "$BACKUP_DIR" -type f -name "${DB_NAME}_*.sql.gz" -mtime +$RETENTION_DAYS -print -delete >> "$LOG_FILE" 2>&1

echo "🔧 $(date +'%F %T') Очистка завершена." | tee -a "$LOG_FILE"
echo "❤️ $(date +'%F %T') Backup скрипт завершён успешно." | tee -a "$LOG_FILE"

exit 0

#!/usr/bin/env bash

# =============================================
# Описание: Сбор и сохранение статистики входов пользователей
# =============================================

# Файл для ведения журналов
readonly LOG_PATH="/var/log/login_activity.log"

# Функция: Вывод в лог и на экран
function log() {
    local message="$1"
    echo -e "${message}" | tee -a "${LOG_PATH}"
}

# Функция: Подсчёт входов за последние 24 часа
function count_recent_logins() {
    local since_date
    since_date=$(date -d 'yesterday' '+%b %e')
    last -F | grep "${since_date}" | wc -l
}

# Функция: Получение топ-5 пользователей
function top_users() {
    last | awk '{print $1}' \
         | sort \
         | uniq -c \
         | sort -nr \
         | head -n 5
}

# Основной блок
log "👥 Начинаем сбор статистики входов..."

LOGIN_COUNT=$(count_recent_logins)
USER_RANKING=$(top_users)

{
    echo -e "📆 $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "🔢 Входов за последние 24 часа: ${LOGIN_COUNT}"
    echo -e "🏆 Топ-5 пользователей по активности:"
    echo "${USER_RANKING}"
    echo "----------------------------------------"
} >> "${LOG_PATH}"

log "✅ Статистика успешно сохранена."

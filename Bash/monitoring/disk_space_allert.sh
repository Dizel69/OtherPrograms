#!/usr/bin/env bash

# disk_space_alert.sh — проверка заполнения дисков и уведомление по email
# Параметры:
#   THRESHOLD — процент заполнения, выше которого отправляется письмо
#   EMAIL     — адрес для уведомлений

# Настройки
THRESHOLD=90
EMAIL="admin@example.com"
LOG_FILE="/var/log/disk_space_alert.log"
DATE_FMT="+%Y-%m-%d %H:%M:%S"

# Функция логирования
log() {
    echo "$(date "${DATE_FMT}") — $1" | tee -a "${LOG_FILE}"
}

# Функция отправки письма
send_alert() {
    local partition="$1"
    local usage="$2"
    local subject="⚠️ Диск ${partition}: заполнено ${usage}%"
    local body="Внимание! Раздел ${partition} заполнен на ${usage}%.
Пожалуйста, освободите место или расширьте раздел."

    echo -e "${body}" | mail -s "${subject}" "${EMAIL}"
    log "Уведомление отправлено: ${partition} — ${usage}%"
}

# Основная проверка дискового пространства
check_disks() {
    df -h --output=pcent,target | tail -n +2 | while read -r usage target; do
        # Убираем символ '%'
        local pct=${usage%\%}
        if (( pct >= THRESHOLD )); then
            send_alert "${target}" "${pct}"
        fi
    done
}

# Точка входа
main() {
    log "Запуск проверки дискового пространства (порог: ${THRESHOLD}%)"
    check_disks
    log "Проверка завершена"
}

main

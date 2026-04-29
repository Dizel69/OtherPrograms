#!/usr/bin/env bash

# mysql_connection_monitor.sh — мониторинг количества подключений к MySQL

LOG_PATH="/var/log/mysql_conn_watch.log"
THRESHOLD=100
DATE_FMT="+%Y-%m-%d %H:%M:%S"

# Настройки подключения (лучше вынести в ~/.my.cnf)
MYSQL_USER="root"
MYSQL_CMD="mysql -u ${MYSQL_USER} -N -s"

log() {
    echo "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_PATH}"
}

get_connections() {
    ${MYSQL_CMD} -e "SHOW STATUS LIKE 'Threads_connected';" 2>/dev/null | awk '{print $2}'
}

check_connections() {
    local conn_count
    conn_count="$(get_connections)"

    if [[ -z "${conn_count}" ]]; then
        log "❌ Не удалось получить данные от MySQL"
        return 1
    fi

    if (( conn_count > THRESHOLD )); then
        log "⚠️ Подключений слишком много: ${conn_count} (порог: ${THRESHOLD})"
    else
        log "✅ Подключения в норме: ${conn_count}"
    fi
}

main() {
    log "🔎 Запуск проверки MySQL подключений"
    check_connections
    log "🔚 Проверка завершена"
}

main
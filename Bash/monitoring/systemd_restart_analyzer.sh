#!/usr/bin/env bash

# systemd_restart_analyzer.sh — анализ частых рестартов сервисов

LOG_FILE="/var/log/systemd_restart_watch.log"
THRESHOLD=3
TIME_WINDOW="1 hour ago"
DATE_FMT="+%Y-%m-%d %H:%M:%S"

log() {
    echo "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_FILE}"
}

get_services() {
    systemctl list-units --type=service --no-legend --no-pager | awk '{print $1}'
}

count_restarts() {
    local service="$1"
    journalctl -u "$service" --since "$TIME_WINDOW" 2>/dev/null | grep -c "Starting"
}

analyze_services() {
    local svc restarts

    while read -r svc; do
        restarts=$(count_restarts "$svc")

        if (( restarts > THRESHOLD )); then
            log "⚠️ Сервис ${svc} перезапускался ${restarts} раз за последний час"
        fi
    done < <(get_services)
}

main() {
    log "🔄 Запуск анализа рестартов systemd (порог: ${THRESHOLD})"
    analyze_services
    log "✅ Анализ завершён"
}

main
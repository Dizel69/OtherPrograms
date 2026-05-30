#!/usr/bin/env bash

# nginx_top_ips.sh — топ IP-адресов по количеству запросов

LOG_PATH="${1:-/var/log/nginx/access.log}"
LIMIT="${2:-10}"
DATE_FMT="+%Y-%m-%d %H:%M:%S"

log() {
    echo "$(date "${DATE_FMT}")  $1"
}

validate_input() {
    if [[ ! -f "$LOG_PATH" ]]; then
        log "❌ Лог-файл не найден: ${LOG_PATH}"
        exit 1
    fi
}

show_top_ips() {
    log "📊 Анализ логов: ${LOG_PATH}"
    echo

    awk '{print $1}' "$LOG_PATH" \
        | sort \
        | uniq -c \
        | sort -nr \
        | head -n "$LIMIT" \
        | awk '{printf "%-15s — %s запросов\n", $2, $1}'
}

main() {
    validate_input
    show_top_ips
    echo
    log "✅ Готово"
}

main
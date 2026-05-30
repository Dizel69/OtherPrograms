#!/usr/bin/env bash

LOG_FILE="/var/log/xsession_monitor.log"
DATE_FMT="+%Y-%m-%d %H:%M:%S"

log() {
    echo -e "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_FILE}"
}

check_sessions() {
    log "🖥 Проверка активных X‑сессий..."
    local sessions
    sessions=$(who | grep -E '(:[0-9]+)' || true)

    if [[ -n "${sessions}" ]]; then
        log "📋 Обнаружены X‑сессии:"
        echo "${sessions}" | tee -a "${LOG_FILE}"
    else
        log "🚫 Активных X‑сессий не найдено"
    fi
}

tail_xorg_log() {
    local xlog="/var/log/Xorg.0.log"
    if [[ -f "${xlog}" ]]; then
        log "🧾 Последние 5 строк из ${xlog}:"
        tail -n 5 "${xlog}" | tee -a "${LOG_FILE}"
    fi
}

main() {
    log "🔍 Старт мониторинга X‑сессий"
    check_sessions
    tail_xorg_log
    log "✅ Мониторинг завершён"
}

main

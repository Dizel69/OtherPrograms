#!/usr/bin/env bash

# systemd_health_check.sh — проверка упавших systemd-сервисов

LOG_PATH="/var/log/systemd_failed_services.log"
TIME_FMT="+%Y-%m-%d %H:%M:%S"

write_log() {
    echo "$(date "${TIME_FMT}")  $1" | tee -a "${LOG_PATH}"
}

get_failed_services() {
    systemctl --failed --no-legend --plain 2>/dev/null
}

report_status() {
    local failed_list
    failed_list="$(get_failed_services)"

    if [[ -z "${failed_list}" ]]; then
        write_log "✅ Сбоев среди systemd-сервисов не обнаружено"
    else
        write_log "❌ Найдены упавшие сервисы:"
        echo "${failed_list}" | tee -a "${LOG_PATH}"
    fi
}

main() {
    write_log "🧭 Запуск проверки systemd"
    report_status
    write_log "🔚 Проверка завершена"
}

main
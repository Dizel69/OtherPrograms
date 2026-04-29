#!/usr/bin/env bash

# long_process_watcher.sh — поиск долго работающих процессов

LOG_PATH="/var/log/stuck_processes.log"
MAX_MINUTES=60
DATE_FMT="+%Y-%m-%d %H:%M:%S"

log() {
    echo "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_PATH}"
}

scan_processes() {
    local pid runtime cmd

    ps -eo pid,etimes,comm --no-headers | \
    while read -r pid runtime cmd; do

        # etimes — время жизни процесса в секундах
        if (( runtime > MAX_MINUTES * 60 )); then
            local minutes=$(( runtime / 60 ))
            log "⚠️ PID=${pid} | runtime=${minutes} min | cmd=${cmd}"
        fi

    done
}

main() {
    log "⏱️ Запуск проверки процессов (порог: ${MAX_MINUTES} мин)"
    scan_processes
    log "✅ Проверка завершена"
}

main
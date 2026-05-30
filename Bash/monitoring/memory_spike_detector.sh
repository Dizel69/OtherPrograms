#!/usr/bin/env bash

# memory_spike_detector.sh — поиск процессов с высоким потреблением RAM

LOG_PATH="/var/log/memory_spike.log"
THRESHOLD_MB=500
DATE_FMT="+%Y-%m-%d %H:%M:%S"

log() {
    echo "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_PATH}"
}

scan_memory() {
    local pid cmd rss_kb mem_mb

    ps -eo pid,comm,rss --sort=-rss --no-headers | \
    while read -r pid cmd rss_kb; do

        # rss в килобайтах → переводим в мегабайты
        mem_mb=$(( rss_kb / 1024 ))

        if (( mem_mb > THRESHOLD_MB )); then
            log "⚠️ PID=${pid} | RAM=${mem_mb}MB | cmd=${cmd}"
        fi

    done
}

main() {
    log "📊 Старт проверки памяти (порог: ${THRESHOLD_MB}MB)"
    scan_memory
    log "✅ Проверка завершена"
}

main
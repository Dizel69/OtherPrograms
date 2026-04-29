#!/usr/bin/env bash

# inode_usage_monitor.sh — мониторинг использования inode на файловых системах

LOG_PATH="/var/log/inode_watch.log"
THRESHOLD=85
DATE_FMT="+%Y-%m-%d %H:%M:%S"

log() {
    echo "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_PATH}"
}

collect_fs_data() {
    df \
        --output=target,itotal,iused,ipcent \
        -x tmpfs -x devtmpfs -x overlay -x squashfs \
        | tail -n +2
}

check_inodes() {
    local mount total used percent

    while read -r mount total used percent; do
        # убираем символ %
        percent=${percent%\%}

        if (( percent >= THRESHOLD )); then
            log "⚠️ ${mount} — inode usage ${percent}% (${used}/${total})"
        fi

    done
}

main() {
    log "🧮 Старт проверки inode (порог: ${THRESHOLD}%)"
    collect_fs_data | check_inodes
    log "✅ Проверка завершена"
}

main
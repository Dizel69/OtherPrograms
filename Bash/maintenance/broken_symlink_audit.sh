#!/bin/bash

# broken_symlink_audit.sh — поиск битых симлинков
# Использование: ./broken_symlink_audit.sh [ROOT]

set -o errexit
set -o nounset
set -o pipefail

ROOT="${1:-/}"
LOG_FILE="/var/log/broken_symlinks.log"
TMP_FILE="$(mktemp)"

cleanup() {
    rm -f "$TMP_FILE"
}
trap cleanup EXIT

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

scan_links() {
    sudo find "$ROOT" -xdev -xtype l -print 2>/dev/null | sort -u > "$TMP_FILE"
}

report_results() {
    local count
    count=$(wc -l < "$TMP_FILE")

    if [[ "$count" -eq 0 ]]; then
        log "✅ Битые симлинки не найдены в ${ROOT}"
    else
        log "⚠️ Найдено битых симлинков: ${count}"
        cat "$TMP_FILE" | tee -a "$LOG_FILE"
    fi
}

main() {
    log "🔗 Запуск поиска битых симлинков в ${ROOT}"
    scan_links
    report_results
    log "✅ Проверка завершена"
}

main
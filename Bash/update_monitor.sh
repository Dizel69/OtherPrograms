#!/bin/bash

LOG_FILE="/var/log/apt_update_check.log"
DATE_CMD="date '+%Y-%m-%d %H:%M:%S'"

function log() {
    local msg="$1"
    echo -e "$(eval $DATE_CMD)  $msg" | tee -a "$LOG_FILE"
}

function update_lists() {
    log "🔄 Обновление списка пакетов (apt update)..."
    if ! sudo apt update -qq; then
        log "❗ Ошибка при обновлении списков пакетов"
        exit 1
    fi
}

function check_upgrades() {
    local upgrades
    upgrades=$(apt list --upgradable 2>/dev/null | grep -v "Listing")
    if [[ -n "$upgrades" ]]; then
        log "📦 Найдены доступные обновления:"
        echo "$upgrades" | tee -a "$LOG_FILE"
    else
        log "✅ Все пакеты уже актуальны"
    fi
}

function main() {
    log "🛠️  Старт проверки APT"
    update_lists
    check_upgrades
    log "🧾 Проверка завершена"
}

main

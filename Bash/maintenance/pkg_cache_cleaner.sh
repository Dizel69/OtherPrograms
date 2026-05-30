#!/usr/bin/env bash

# pkg_cache_cleaner.sh — очистка кэша пакетных менеджеров

LOG_FILE="/var/log/pkg_cache_cleaner.log"
DATE_FMT="+%Y-%m-%d %H:%M:%S"

log() {
    echo "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_FILE}"
}

detect_manager() {
    if command -v apt >/dev/null 2>&1; then
        echo "apt"
    elif command -v dnf >/dev/null 2>&1; then
        echo "dnf"
    elif command -v pacman >/dev/null 2>&1; then
        echo "pacman"
    else
        echo "unknown"
    fi
}

clean_apt() {
    log "🧹 Очистка APT cache"
    sudo apt clean >> "$LOG_FILE" 2>&1
    sudo apt autoclean >> "$LOG_FILE" 2>&1
}

clean_dnf() {
    log "🧹 Очистка DNF cache"
    sudo dnf clean all >> "$LOG_FILE" 2>&1
}

clean_pacman() {
    log "🧹 Очистка Pacman cache"
    sudo pacman -Sc --noconfirm >> "$LOG_FILE" 2>&1
}

main() {
    log "🔍 Определение пакетного менеджера..."

    case "$(detect_manager)" in
        apt)
            clean_apt
            ;;
        dnf)
            clean_dnf
            ;;
        pacman)
            clean_pacman
            ;;
        *)
            log "❌ Пакетный менеджер не определён"
            exit 1
            ;;
    esac

    log "✅ Очистка завершена"
}

main
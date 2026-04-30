#!/usr/bin/env bash

# host_ping_checker.sh — проверка доступности хостов

TARGETS=("192.168.0.1" "google.com" "yandex.ru" "192.168.0.100")
LOG_FILE="/var/log/host_ping_checker.log"
DATE_FMT="+%Y-%m-%d %H:%M:%S"

# Цвета
CLR_OK="\033[0;32m"
CLR_FAIL="\033[0;31m"
CLR_RESET="\033[0m"

log() {
    echo "$(date "${DATE_FMT}")  $1" >> "$LOG_FILE"
}

check_host() {
    local host="$1"

    if ping -c 1 -W 1 "$host" >/dev/null 2>&1; then
        echo -e "${CLR_OK}[UP]   ${host}${CLR_RESET}"
        log "[UP] ${host}"
    else
        echo -e "${CLR_FAIL}[DOWN] ${host}${CLR_RESET}"
        log "[DOWN] ${host}"
    fi
}

main() {
    for target in "${TARGETS[@]}"; do
        check_host "$target"
    done
}

main
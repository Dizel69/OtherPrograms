#!/usr/bin/env bash

# usb_state_monitor.sh — отслеживание изменений USB-устройств

LOG_PATH="/var/log/usb_changes.log"
STATE_DIR="/var/lib/usb_changes"
STATE_FILE="${STATE_DIR}/usb_state.txt"
TMP_FILE="/tmp/usb_current.$$"
DATE_FMT="+%Y-%m-%d %H:%M:%S"

log() {
    echo "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_PATH}"
}

prepare() {
    mkdir -p "${STATE_DIR}"
}

collect_usb_state() {
    lsusb > "${TMP_FILE}"
}

first_run() {
    cp "${TMP_FILE}" "${STATE_FILE}"
    log "📦 Инициализация: сохранено начальное состояние USB"
}

compare_states() {
    if ! diff -u "${STATE_FILE}" "${TMP_FILE}" >/dev/null; then
        log "⚠️ Обнаружены изменения USB-устройств"

        log "--- Было:"
        cat "${STATE_FILE}" | tee -a "${LOG_PATH}"

        log "--- Стало:"
        cat "${TMP_FILE}" | tee -a "${LOG_PATH}"

        cp "${TMP_FILE}" "${STATE_FILE}"
    else
        log "✅ Изменений не обнаружено"
    fi
}

cleanup() {
    rm -f "${TMP_FILE}"
}

main() {
    log "🔍 Запуск проверки USB"
    prepare
    collect_usb_state

    if [[ ! -f "${STATE_FILE}" ]]; then
        first_run
        cleanup
        exit 0
    fi

    compare_states
    cleanup

    log "🔚 Проверка завершена"
}

main
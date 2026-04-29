#!/usr/bin/env bash

# tls_cert_watcher.sh — мониторинг срока действия TLS-сертификатов

LOG_PATH="/var/log/tls_expiry_check.log"
THRESHOLD_DAYS=30
DATE_FMT="+%Y-%m-%d %H:%M:%S"

# Список хостов (формат: host или host:port)
TARGETS=(
    "example.com"
    "api.example.com:443"
    "github.com"
)

log() {
    echo "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_PATH}"
}

parse_target() {
    local entry="$1"
    local host port

    host="${entry%:*}"
    port="${entry#*:}"

    [[ "${host}" == "${port}" ]] && port=443

    echo "${host} ${port}"
}

get_cert_expiry() {
    local host="$1"
    local port="$2"

    timeout 10 bash -c "
        echo | openssl s_client -servername ${host} -connect ${host}:${port} 2>/dev/null \
        | openssl x509 -noout -enddate 2>/dev/null
    " | sed 's/^notAfter=//'
}

check_target() {
    local entry="$1"
    local host port end_date end_ts now_ts days_left

    read -r host port < <(parse_target "$entry")

    end_date="$(get_cert_expiry "$host" "$port")"

    if [[ -z "${end_date}" ]]; then
        log "❌ ${host}:${port} — не удалось получить сертификат"
        return
    fi

    end_ts=$(date -d "${end_date}" +%s 2>/dev/null)
    now_ts=$(date +%s)

    if [[ -z "${end_ts}" ]]; then
        log "❌ ${host}:${port} — ошибка парсинга даты (${end_date})"
        return
    fi

    days_left=$(( (end_ts - now_ts) / 86400 ))

    if (( days_left <= THRESHOLD_DAYS )); then
        log "⚠️ ${host}:${port} — истекает через ${days_left} дн (до ${end_date})"
    else
        log "✅ ${host}:${port} — ${days_left} дн до истечения"
    fi
}

main() {
    log "🔐 Старт проверки TLS-сертификатов (порог: ${THRESHOLD_DAYS} дней)"

    for target in "${TARGETS[@]}"; do
        check_target "${target}"
    done

    log "🔚 Проверка завершена"
}

main
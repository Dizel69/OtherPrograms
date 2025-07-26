#!/usr/bin/env bash

# apt_cleanup_manager.sh — автоматическая очистка системы пакетов APT с логированием

LOG_FILE="/var/log/apt_cleanup.log"
DATE_FMT="+%Y-%m-%d %H:%M:%S"

# Функция логирования сообщений с таймстампом
log() {
    echo -e "$(date "${DATE_FMT}")  $1" | tee -a "${LOG_FILE}"
}

# Удаление неиспользуемых зависимостей
remove_unused() {
    log "🧹 Запуск apt autoremove"
    if sudo apt autoremove -y >> "${LOG_FILE}" 2>&1; then
        log "✔️  Зависимости удалены"
    else
        log "❗ Ошибка при удалении зависимостей"
    fi
}

# Очистка кэша пакетов
clean_cache() {
    log "🗄️  Запуск apt clean"
    if sudo apt clean >> "${LOG_FILE}" 2>&1; then
        log "✔️  Кэш пакетов очищен"
    else
        log "❗ Ошибка при очистке кэша"
    fi
}

# Очистка устаревших пакетов из локального кэша
autoclean_cache() {
    log "🗑️  Запуск apt autoclean"
    if sudo apt autoclean >> "${LOG_FILE}" 2>&1; then
        log "✔️  Локальный кэш обновлён"
    else
        log "❗ Ошибка при autoclean"
    fi
}

main() {
    log "🛠️  Старт очистки APT"
    remove_unused
    clean_cache
    autoclean_cache
    log "✅ Очистка APT завершена"
}

main

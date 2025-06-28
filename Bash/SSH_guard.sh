#!/usr/bin/env bash

# ============================================
# Описание: Анализ неудачных SSH-попыток и вывод ТОП-10 IP-адресов
# ============================================

# Путь к файлу логов (CentOS: /var/log/secure)
readonly AUTH_LOG="/var/log/auth.log"
# Сколько IP-адресов показывать
readonly TOPN=10

# Функция: Вывод заголовка
print_header() {
    echo -e "🔍 Анализ неудачных SSH-попыток"
    echo -e "🚨 Топ ${TOPN} IP-адресов с ошибками входа:"
}

# Функция: Извлечение и подсчёт неудачных попыток
analyze_failures() {
    grep -E "Failed password for" "${AUTH_LOG}" \
        | grep -oP '(?<=from )[0-9.]+(?= port)' \
        | sort \
        | uniq -c \
        | sort -rn \
        | head -n "${TOPN}"
}

# Основная логика
print_header
analyze_failures

# Завершение
echo -e "✅ Готово!"

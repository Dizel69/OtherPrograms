#!/bin/bash

# Мониторинг процессов по загрузке CPU и памяти

# Настройки порогов (в процентах)
MAX_CPU=80
MAX_MEM=70

LOG_FILE="/var/log/high_resource_processes.log"

function banner() {
    echo -e "\n🔥 Проверка процессов..."
}

function report_high_cpu() {
    echo -e "\n🔍 Процессы с CPU > ${MAX_CPU}%:"
    ps -eo pid,comm,%cpu --no-headers | \
        awk -v thr="$MAX_CPU" '$3 > thr' | \
        sort -k3 -nr
}

function report_high_mem() {
    echo -e "\n🔍 Процессы с MEM > ${MAX_MEM}%:"
    ps -eo pid,comm,%mem --no-headers | \
        awk -v thr="$MAX_MEM" '$3 > thr' | \
        sort -k3 -nr
}

function log_suspects() {
    echo -e "\n📝 Логирование процессов в ${LOG_FILE}..."
    ps -eo pid,comm,%cpu,%mem --no-headers | \
        awk -v cpu="$MAX_CPU" -v mem="$MAX_MEM" '$3 > cpu || $4 > mem' | \
        sort -k3,3nr -k4,4nr >> "${LOG_FILE}"
}

# Основной запуск
banner
report_high_cpu
report_high_mem
log_suspects

echo -e "\n✅ Проверка завершена.\n"

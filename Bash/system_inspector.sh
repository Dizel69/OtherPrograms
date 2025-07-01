#!/usr/bin/env bash

# =============================================
# Описание: Сбор подробной информации о системе
# =============================================

# Файл для вывода результатов (по умолчанию вывод на экран)
readonly OUTPUT=""

# Функция: вывод заголовка секции
print_section() {
    local title="$1"
    echo -e "\n🔹 ===== $title ===== 🔹" | tee -a "${OUTPUT}" 2>/dev/null
}

# Функция: выполнение команды и логирование
run_cmd() {
    local cmd_desc="$1"
    local cmd="$2"
    print_section "${cmd_desc}"
    eval "${cmd}" | tee -a "${OUTPUT}" 2>/dev/null
}

# Основные проверки
run_cmd "Общая информация о системе (uname, hostnamectl)" "uname -a; hostnamectl"
run_cmd "Информация о CPU" "lscpu"
run_cmd "Информация о памяти" "free -h; cat /proc/meminfo"
run_cmd "Физические модули памяти (dmidecode)" "sudo dmidecode --type memory"
run_cmd "Информация о дисках и разделах" "lsblk; df -h"
run_cmd "Информация о видеокарте" "lspci | grep -i vga"
run_cmd "Список USB-устройств" "lsusb"
run_cmd "Подробная информация о блоках устройств" "sudo lshw -short"

echo -e "\n✅ Сбор информации завершён." | tee -a "${OUTPUT}" 2>/dev/null

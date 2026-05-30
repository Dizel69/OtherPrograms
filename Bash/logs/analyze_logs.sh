#!/bin/bash
LOG_FILE="$(dirname "$0")/logs"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "Файл логов не найден: $LOG_FILE"
    exit 1
fi

# Предполагаем, что в логе строка с "unreachable" считается ошибкой
grep -iE "bad|error|fail" "$LOG_FILE"
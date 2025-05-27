#!/bin/bash

# Конфигурация
BOT_TOKEN="your_bot_token"
CHAT_ID="your_chat_id"
CACHE_FILE="/var/tmp/open_ports_last.txt"
CURRENT_FILE="/tmp/current_ports.txt"

# Сбор открытых TCP/UDP портов
ss -tuln | awk 'NR > 1 {split($5, a, ":"); print a[length(a)]}' | sort -n | uniq > "$CURRENT_FILE"

# Если файл с предыдущим состоянием отсутствует — создаём его и завершаем скрипт
if [[ ! -f "$CACHE_FILE" ]]; then
    cp "$CURRENT_FILE" "$CACHE_FILE"
    exit 0
fi

# Поиск изменений
CHANGES=$(diff -u "$CACHE_FILE" "$CURRENT_FILE")

# Если есть различия — отправляем уведомление в Telegram
if [[ -n "$CHANGES" ]]; then
    TEXT="⚠️ Изменения в открытых портах:\n\`\`\`\n$CHANGES\n\`\`\`"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d parse_mode="Markdown" \
        -d text="$TEXT"

    cp "$CURRENT_FILE" "$CACHE_FILE"
fi

# Очистка временного файла
rm -f "$CURRENT_FILE"

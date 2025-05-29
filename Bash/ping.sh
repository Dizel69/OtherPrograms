#!/usr/bin/env bash
LOG_FILE="$(dirname "$0")/logs"

while true; do
    TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
    if ping -c 4 -W 2 8.8.8.8 &>/dev/null; then
        echo "${TIMESTAMP} - 8.8.8.8 OK" >> "$LOG_FILE"
    else
        echo "${TIMESTAMP} - 8.8.8.8 bad" >> "$LOG_FILE"
    fi
    sleep 1800  # 30 minutes
done
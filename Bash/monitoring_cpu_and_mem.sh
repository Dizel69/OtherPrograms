#!/bin/bash
LOG_FILE="/var/log/high_cpu_mem_pids.log"
CPU_TH=90
MEM_TH=60

while true; do
    date_stamp="$(date '+%d,%m,%Y,%H,%M:%S')"
    ps -eo pid,pcpu,pmem,comm --no-headers | \
        awk -v cth="$CPU_TH" -v mth="$MEM_TH" -v ds="$date_stamp" \
            '$2 > cth || $3 > mth {print ds","$1","$4}' >> "$LOG_FILE"
    sleep 5
    done
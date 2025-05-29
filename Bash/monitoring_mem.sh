#!/bin/bash
LOG_FILE="/var/log/high_mem_pids.log"
THRESHOLD=60

while true; do
    date_stamp="$(date '+%d,%m,%Y,%H,%M,%S')"
    ps -eo pid,pmem,comm --no-headers | \
        awk -v thr="$THRESHOLD" -v ds="$date_stamp" '$2 > thr {print ds","$1","$3}' >> "$LOG_FILE"
    sleep 5
done
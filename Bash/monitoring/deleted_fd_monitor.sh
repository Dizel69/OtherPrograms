#!/bin/bash

LOG_FILE="/var/log/open_deleted_files.log"
MIN_SIZE_MB=100   # Порог размера «висящего» файла для отчёта (в МБ)

echo "🗑 Поиск открытых удалённых файлов... $(date)" | tee -a "$LOG_FILE"

# Требуется lsof; лучше запускать с sudo для полноты картины
if ! command -v lsof >/dev/null 2>&1; then
  echo "❌ Не найден lsof. Установите пакет lsof." | tee -a "$LOG_FILE"
  exit 1
fi

# Выдаёт: PID|FD|SIZE(bytes)|CMD|USER|NAME
sudo lsof +L1 -nP 2>/dev/null | awk '
  NR>1 {
    cmd=$1; pid=$2; user=$3; fd=$4; size=$7;
    name="";
    for (i=9;i<=NF;i++) name=name $i " ";
    gsub(/^[ \t]+|[ \t]+$/,"",name);
    gsub(/[a-zA-Z]+$/,"",fd);        # оставить только номер FD
    gsub(/[^0-9]/,"",size); if (size=="") size=0;  # очистить SIZE/OFF
    print pid "|" fd "|" size "|" cmd "|" user "|" name
  }' \
| while IFS='|' read -r PID FD BYTES CMD USER NAME; do
    MB=$(( (BYTES + 1024*1024 - 1) / (1024*1024) ))
    if [ "$MB" -ge "$MIN_SIZE_MB" ]; then
      echo "⚠️ PID:$PID USER:$USER CMD:$CMD FD:$FD SIZE:${MB}MB NAME:${NAME}" | tee -a "$LOG_FILE"

      # 🔽 Опционально: аккуратно освободить место, обнулив дескриптор (НЕ по умолчанию!)
      # Использовать осторожно и только для безопасных логов, НИКОГДА для БД/критичных файлов.
      # if [ -e "/proc/$PID/fd/$FD" ]; then
      #   : > "/proc/$PID/fd/$FD" && echo "🧹 Освобождён дескриптор /proc/$PID/fd/$FD" | tee -a "$LOG_FILE"
      # fi
    fi
  done

echo "✅ Проверка завершена." | tee -a "$LOG_FILE"

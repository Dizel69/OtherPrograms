#!/bin/bash

# Задаём путь к целевой папке
TARGET_DIR="/home/march/nielsen/wildparser/csv"

# Проверяем, существует ли папка
if [ ! -d "$TARGET_DIR" ]; then
  echo "Папка $TARGET_DIR не существует. Завершаем выполнение."
  exit 1
fi

# Находим и удаляем файлы старше 30 дней, исключая папку input/
find "$TARGET_DIR" \
  -path "$TARGET_DIR/input" -prune -o \
  -type f -mtime +30 -exec rm -f {} \;

echo "Удалены файлы старше 30 дней из папки $TARGET_DIR, за исключением папки input/."

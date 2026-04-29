#!/bin/bash

# Имя файла для записи контрольных сумм
touch distr.md5
MD5_FILE="distr.md5"

# Очищаем/создаем файл
> "$MD5_FILE"

# Обрабатываем все deb-файлы в текущей директории
for deb_file in *.deb; do
    # Проверяем, что файл существует (на случай, если нет deb-файлов)
    if [ -f "$deb_file" ]; then
        # Вычисляем MD5 и извлекаем только хэш (первое поле)
        md5_hash=$(md5sum "$deb_file" | cut -d' ' -f1)
        # Записываем в формате: "хэш - имя_файла"
        echo "$md5_hash - $deb_file" >> "$MD5_FILE"
    fi
done

# Сообщаем о завершении
if [ -s "$MD5_FILE" ]; then
    echo "Контрольные суммы записаны в $MD5_FILE"
    echo "Содержимое файла:"
    cat "$MD5_FILE"
else
    echo "В текущей директории не найдено deb-пакетов"
fi

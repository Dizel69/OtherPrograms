#!/bin/bash
# Проверка входных параметров: должно быть 2 аргумента (название пакета и версия)
if [ "$#" -ne 2 ]; then
    echo "Использование: $0 <название_пакета> <версия>"
    exit 1
fi

main_package="$1"
main_version="$2"
max_depth=3  # Максимальная глубина вложенности

# Функция для рекурсивного получения зависимостей и их выводa в виде дерева.
# Параметры:
#   $1 – имя пакета
#   $2 – версия пакета (если есть, иначе пустая строка)
#   $3 – оставшаяся глубина обхода
#   $4 – префикс для оформления вывода (отступ с символами дерева)
get_dependencies() {
    local package=$1
    local version=$2
    local depth=$3
    local prefix=$4

    # Выводим название пакета и версию (если версия задана)
    if [ -z "$prefix" ]; then
        if [ -n "$version" ]; then
            echo "${package}==${version}"
        else
            echo "${package}"
        fi
    else
        if [ -n "$version" ]; then
            echo "${prefix}└── ${package}==${version}"
        else
            echo "${prefix}└── ${package}"
        fi
    fi

    # Если достигнута максимальная глубина (текущий уровень – последний), прекращаем рекурсию.
    if [ "$depth" -le 1 ]; then
        return
    fi

    # Формируем URL для запроса JSON через API PyPI.
    local url=""
    if [ -n "$version" ]; then
        url="https://pypi.python.org/pypi/${package}/${version}/json"
    else
        url="https://pypi.python.org/pypi/${package}/json"
    fi

    # Получаем JSON с информацией о пакете.
    local json
    json=$(curl -s -L "$url")

    # Извлекаем зависимости из поля requires_dist (если оно есть).
    local deps
    deps=$(echo "$json" | jq -r '.info.requires_dist[]? // empty')

    if [ -z "$deps" ]; then
        return
    fi

    # Для вложенных зависимостей увеличиваем префикс (4 пробела к текущему отступу).
    local new_prefix="${prefix}    "

    # Перебираем каждую зависимость.
    while IFS= read -r dep; do
         # Извлекаем имя зависимости (первый токен).
         local dep_name
         dep_name=$(echo "$dep" | awk '{print $1}')

         # Извлекаем версию зависимости, если она задана в виде (==<версия>).
         # Используем grep для извлечения строки, следующей после "==", до закрывающей скобки.
         local dep_version
         dep_version=$(echo "$dep" | grep -oP '\(\s*==\s*\K[^)]+')
         dep_version=$(echo "$dep_version" | xargs)  # Убираем лишние пробелы

         # Рекурсивно обрабатываем зависимость, уменьшая глубину обхода.
         get_dependencies "$dep_name" "$dep_version" $((depth - 1)) "$new_prefix"
    done <<< "$deps"
}

# Выводим дерево зависимостей основного пакета.
get_dependencies "$main_package" "$main_version" "$max_depth" ""
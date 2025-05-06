#!/bin/bash

REQ_FILE="requirements.txt"
DEVPI_URL="http://адрес:8085/packages/releases"

while IFS= read -r line || [[ -n "$line" ]]; do
  
  # Разбиваем на пакет и версию (игнорируем условия после ;)
  package=$(echo "$line" | awk -F'==' '{print $1}' | awk -F';' '{print $1}' | tr -d ' ')
  version=$(echo "$line" | awk -F'==' '{print $2}' | awk -F';' '{print $1}' | tr -d ' ')
  
  # Формируем URL
  url="${DEVPI_URL}/${package}/${version}"
  
  # Делаем запрос и парсим JSON
  curl --header "Accept: application/json" "$url" | \
    jq -r '.result."+links"[] | select(.href | contains("tar.gz")) | .href'

done < "$REQ_FILE"

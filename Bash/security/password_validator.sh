#!/usr/bin/env bash

# Требования:
# - минимум 8 символов
# - хотя бы одна заглавная буква
# - хотя бы одна строчная буква
# - хотя бы одна цифра
# - хотя бы один специальный символ

function prompt_password() {
    read -s -p "Введите пароль: " pass
    echo
}

function validate_password() {
    local pw="$1"
    local length_ok pattern_ok=0

    # Проверяем длину
    if (( ${#pw} < 8 )); then
        echo "❌ Пароль слишком короткий (минимум 8 символов)"
        return 1
    fi

    # Проверка наличия разных классов символов
    [[ "$pw" =~ [A-Z] ]] && ((pattern_ok++))
    [[ "$pw" =~ [a-z] ]] && ((pattern_ok++))
    [[ "$pw" =~ [0-9] ]] && ((pattern_ok++))
    [[ "$pw" =~ [^a-zA-Z0-9] ]] && ((pattern_ok++))

    if (( pattern_ok == 4 )); then
        echo "✅ Надёжный пароль"
        return 0
    else
        echo "❌ Слабый пароль:"
        echo "   - Требуется минимум 1 заглавная буква"  # даже если уже есть, выводим общий список
        echo "   - Требуется минимум 1 строчная буква"
        echo "   - Требуется минимум 1 цифра"
        echo "   - Требуется минимум 1 специальный символ"
        return 1
    fi
}

# Основной цикл — повторяем до тех пор, пока пароль не будет валидным
while true; do
    prompt_password
    if validate_password "$pass"; then
        break
    fi
    echo "Попробуйте ещё раз."
done

# Используем официальный образ Python 3.9
FROM python:3.12-slim

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]

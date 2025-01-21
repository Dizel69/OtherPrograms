# Базовый образ с Python 3
FROM python:3.9-slim

# Установим рабочую директорию внутри контейнера
WORKDIR /app

# Скопируем файл зависимостей
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем всё приложение
COPY . .

# Укажем порт, который будет использоваться
EXPOSE 5000

# Запустим приложение
CMD ["python", "app.py"]

# Используем официальный образ Python (например, версию 3.9 на slim базе)
FROM python:3.9-slim

# Задаём рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Открываем порт, который будет использовать Flask
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]

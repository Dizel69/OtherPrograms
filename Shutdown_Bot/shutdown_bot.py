from telegram import Update
from telegram.ext import Application, CommandHandler
import subprocess
import os

# Токен вашего Telegram-бота
BOT_TOKEN = 'ваш токен'

# Функция для запуска Python-скрипта напрямую
async def start_parser(update: Update, context):
    try:
        # Запуск скрипта parser.py
        process = subprocess.Popen(['python3', '/home/dizel/PycharmProjects/wildparser/parser.py'], shell=False)
        await update.message.reply_text('Проект запущен напрямую!')
    except Exception as e:
        await update.message.reply_text(f'Ошибка запуска проекта: {e}')

# Функция для остановки процесса Python (если необходимо)
async def stop_parser(update: Update, context):
    try:
        # Остановка процессов с именем parser.py
        subprocess.Popen(['pkill', '-f', 'parser.py'], shell=False)
        await update.message.reply_text('Проект остановлен!')
    except Exception as e:
        await update.message.reply_text(f'Ошибка остановки проекта: {e}')

# Функция приветствия с выводом доступных команд
async def start(update: Update, context):
    commands = """
Привет! Вот доступные команды:
/shutdown - Выключение системы😭
/run_pycharm - Запуск Pycharm😊
"""
    await update.message.reply_text(commands)

# Функция для выключения системы
async def shutdown(update: Update, context):
    try:
        await update.message.reply_text('Выключение системы...😭')
        subprocess.Popen(['sudo', 'shutdown', '-h', 'now'], shell=False)
    except Exception as e:
        await update.message.reply_text(f'Ошибка при попытке выключения системы: {e}')

def runpycharm(update: Update, context):
    update.message.reply_text("Запуск PyCharm...")
    subprocess.Popen(["/snap/pycharm-community/414/bin/pycharm.sh"])

# Главная функция для запуска бота
def main():
    # Инициализация бота с использованием Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Команда для приветственного сообщения
    application.add_handler(CommandHandler('start', start))

    # Команда для запуска проекта
    #application.add_handler(CommandHandler('start_parser', start_parser))

    # Команда для остановки проекта
    #application.add_handler(CommandHandler('stop_parser', stop_parser))

    # Команда для выключения системы
    application.add_handler(CommandHandler('shutdown', shutdown))

    #Команда для запуска PyCharm
    application.add_handler(CommandHandler('run_pycharm', runpycharm))

    # Запуск бота
    application.run_polling()

# Точка входа в программу
if __name__ == '__main__':
    main()

#/start_parser - Запуск проекта напрямую
#/stop_parser - Остановка проекта
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = 'Токен_Вашего_Бота'

# Функция для выключения системы
async def shutdown(update: Update, context):
    await update.message.reply_text('Выключение системы...')
    os.system('sudo shutdown now')

# Основная функция для запуска бота
async def start(update: Update, context):
    await update.message.reply_text('Привет! Используй команду /shutdown для выключения системы.')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Команда для запуска
    app.add_handler(CommandHandler('start', start))

    # Команда для выключения
    app.add_handler(CommandHandler('shutdown', shutdown))

    print("Бот запущен. Ожидание команд.")
    app.run_polling()


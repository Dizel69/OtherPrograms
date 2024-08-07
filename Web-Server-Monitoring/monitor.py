import requests
import smtplib
import logging
import time
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройка логирования
logging.basicConfig(filename='logs/monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Загрузка конфигурации из файла config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Функция для отправки уведомления на email
def send_email(subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = config['email']['sender']
        msg['To'] = config['email']['recipient']
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(config['email']['smtp_server'], config['email']['smtp_port'])
        server.starttls()
        server.login(config['email']['sender'], config['email']['password'])
        server.send_message(msg)
        server.quit()
        logging.info(f'Email notification sent to {config["email"]["recipient"]}')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')

# Функция для отправки уведомления в Telegram
def send_telegram_message(message):
    try:
        token = config['telegram']['bot_token']
        chat_id = config['telegram']['chat_id']
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info('Telegram notification sent successfully')
        else:
            logging.error(f'Failed to send Telegram message: {response.status_code}')
    except Exception as e:
        logging.error(f'Failed to send Telegram message: {e}')

# Функция для проверки состояния веб-сервера
def check_server_status():
    try:
        response = requests.get(config['url'], timeout=config['timeout'])
        if response.status_code == 200:
            logging.info(f'Server is up: {response.status_code}')
        else:
            logging.warning(f'Server returned status code: {response.status_code}')
            notify_failure(response.status_code)
    except requests.exceptions.RequestException as e:
        logging.error(f'Server is down or unreachable: {e}')
        notify_failure(str(e))

# Функция для отправки уведомления при сбое
def notify_failure(error_message):
    subject = f'Alert: Server {config["url"]} is down'
    message = f'Server {config["url"]} is not responding or returned an error.\n\nError details:\n{error_message}'
    send_email(subject, message)
    send_telegram_message(message)

# Основной цикл проверки с заданным интервалом
if __name__ == '__main__':
    while True:
        check_server_status()
        time.sleep(config['check_interval'] * 60)

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
import psycopg2

# Переменные для настройки Google Sheets
# Путь к файлу учетных данных
CREDENTIALS_FILE = 'C:/Users/dizel/my_testAirFlow/airflow/client.json'

# Имя Google Sheet
GOOGLE_SHEET_NAME = 'имя вашей таблицы'

# Область доступа для API Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Настройка Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
client = gspread.authorize(creds)

# Открываем Google Sheet
spreadsheet = client.open(hhairflow)
sheet = spreadsheet.sheet1

# Получаем все данные из таблицы
data = sheet.get_all_records()

# Преобразуем данные в DataFrame
df = pd.DataFrame(data)

# Определяем столбцы для Excel файла
COLUMNS = [
    "Имя и фамилия", "Адрес эл. почты", "Номер телефона", "Возраст",
    "Опыт работы", "Ссылка на резюме", "Ожидаемая зп", "Занятость",
    "Специализация", "График работы"
]

# Убеждаемся, что DataFrame содержит эти столбцы
df = df[COLUMNS]

# Сохраняем в Excel файл
df.to_excel("data.xlsx", index=False)

# Переменные для настройки PostgreSQL
POSTGRES_USER = 'admin'
POSTGRES_PASSWORD = 'admin'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'postgres'

# Строка подключения к PostgreSQL
DATABASE_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# Настройка PostgreSQL
engine = create_engine(DATABASE_URL)

# Вставляем данные в PostgreSQL
TABLE_NAME = 'data.xlsx'
df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)

print("Данные успешно получены из Google Sheets, вставлены в PostgreSQL и сохранены в Excel.")
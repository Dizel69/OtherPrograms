# Data Extraction and Storage Script

Этот проект предназначен для извлечения данных из Google Sheets, их сохранения в базе данных PostgreSQL, работающей в Docker, и записи данных в файл Excel.

## Предварительные требования

- Docker
- Учетная запись Google и доступ к Google Cloud Console
- Python 3
- Файл учетных данных `client_secret.json` для Google Sheets API
- docker-compose скачиваем с официального сайта


## Переменные окружения

| Переменная               | Описание                                                          | Значение по умолчанию                  |
|--------------------------|-------------------------------------------------------------------|----------------------------------------|
| `CREDENTIALS_FILE`       | Путь к файлу учетных данных для Google Sheets API.                |                                        |
| `GOOGLE_SHEET_NAME`      | Имя Google Sheet, из которого будут извлекаться данные.           | `hhairflow`                            |
| `SCOPE`                  | Область доступа для Google Sheets API.                            |                                        |
| `COLUMNS`                | Список столбцов, которые должны быть в DataFrame и в Excel файле. |                                        |
| `POSTGRES_USER`          | Имя пользователя для подключения к PostgreSQL.                    | `admin`                                |
| `POSTGRES_PASSWORD`      | Пароль пользователя для подключения к PostgreSQL.                 | `admin`                                |
| `POSTGRES_HOST`          | Путь к файлу учетных данных для Google Sheets API.                | `localhost`                            |
| `POSTGRES_PORT`          | Порт базы данных PostgreSQL.                                      | `ваш порт`                             |
| `POSTGRES_DB`            | Имя базы данных PostgreSQL.                                       | `postgres`                             |
| `DATABASE_URL`           | Строка подключения к базе данных PostgreSQL.                      | `Собирается из указанных переменных`   |
| `TABLE_NAME`             | Имя таблицы в базе данных Postgres, куда будут вставляться данные | `data.xlsx`                            |
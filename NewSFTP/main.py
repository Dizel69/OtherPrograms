import fnmatch
import logging
import os
import sqlite3
import schedule
from core.configuration import parseConfig, config
from core.email import send_tech_data_emails, send_emails
from core.sftpConnection import create_sftp, LocalFileServer

# Настройка логирования и подключения к базе данных:
# Здесь происходит настройка логирования, которое записывается
# в файл main.log. Также создается подключение к базе данных SQLite с файлом fs.db.
con = sqlite3.connect("fs.db")

logging.basicConfig(
    filename="main.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger("mainLogger")


# Функция создает подключение к серверу на основе типа сервера SFTP
def srs(server):
    try:
        if server["type"] == "sftp":
            return create_sftp(server)
        else:
            return LocalFileServer(server["rootDir"])
    except Exception as e:
        logger.exception("Can't create connection! %s", str(e))
        return None


# Здесь происходит создание подключений ко всем серверам из конфигурации и
# вызов функции prs для обработки файлов. В конце все подключения закрываются.
def process(files):
    servers = [srs(server) for server in config["servers"]]
    sources = [server for server in servers if server is not None]
    prs(files, sources)
    for source in sources:
        source.server.close()


# Эта функция отправляет уведомления по электронной почте о состоянии обработки файлов.
def send_notifications(errors, processed):
    if not processed and not errors:
        logger.info("Nothing to process in this run")
    else:
        send_emails(processed, errors)


# В этой функции происходит основная обработка файлов. Файлы загружаются с источников,
# обрабатываются и отправляются на целевой сервер.
def prs(files, sources):
    errors = []
    processed = []
    for source in sources:
        try:
            for filename in source.files():
                if fnmatch.fnmatch(filename, "*.zip") and filename not in files:
                    local_file = os.path.join(config["temp-dir"], filename)
                    logger.info("Download %s", local_file)
                    source.download(filename, local_file, filename, errors)
                    logger.info("File %s downloaded", filename)
                    try:
                        sftp_target = create_sftp(config["target-server"])
                        remote_file = os.path.join(sftp_target.root_dir, filename)
                        logger.info("Sending %s", remote_file)
                        sftp_target.server.put(local_file, remote_file, confirm=False)
                        sftp_target.server.close()
                        processed.append(f"{source.type}:{source.root_dir} - {filename}")
                        add_file(filename, source.type, os.path.getsize(local_file))
                        logger.info("File %s sent", remote_file)
                    except (IOError, OSError):
                        errors.append(filename)
                        logger.exception("Can't put file to remote server: %s", filename)
                    finally:
                        os.remove(local_file)
        except Exception as e:
            errors.append(source.root_dir)
            logger.exception("Can't get list of files from: %s: %s: %s", source.root_dir, str(type(e)), str(e))
    send_notifications(errors, processed)


# Эта функция добавляет запись о файле в базу данных.
def add_file(filename, source, file_size):
    with con:
        con.execute(
            "INSERT INTO file (file_name, source, file_size) VALUES (?, ?, ?)",
            (filename, source, file_size)
        )


# В этой функции происходит инициализация конфигурации,
# создание таблицы в базе данных (если её нет), и вызов функции process для обработки файлов.
def init():
    parseConfig()
    logger.info("----------------- starting processing -----------------")
    with con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS file(
                file_name   varchar(50),
                source      varchar(10),
                time_update datetime default CURRENT_TIMESTAMP,
                file_size   INTEGER
            )"""
        )
        rows = con.execute("SELECT file_name FROM file").fetchall()
    process([row[0] for row in rows])
    logger.info("----------------       processed      -----------------")


# В этой функции происходит первичная инициализация и настройка
# периодического выполнения задачи с помощью модуля schedule.
def runa():
    try:
        init()
    except Exception as e:
        logger.exception("Oppss.")
        send_tech_data_emails(e)
    import time

    def job():
        try:
            init()
        except Exception as e:
            logger.exception("Oppss.")
            send_tech_data_emails(e)

    schedule.every(config["interval"]).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


# Запуск файла
if __name__ == "__main__":
    runa()

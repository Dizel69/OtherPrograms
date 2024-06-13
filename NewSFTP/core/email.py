import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Эта функция ыполняет общую логику для отправки email-сообщений, тем самым устраняя
# дублирование кода. Она принимает тему письма, текст, список получателей и конфигурацию email.
def send_email(subject, body, recipients, email_conf):
    from_address = email_conf['from_address']
    password = email_conf['password']

    try:
        server = smtplib.SMTP_SSL(email_conf['host'], email_conf['port'])
        server.login(from_address, password)

        for email in recipients:
            try:
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = from_address
                message["To"] = email

                message.attach(MIMEText(body, "plain"))

                server.sendmail(from_address, email, message.as_string())
            except:
                logging.exception("Cant deliver a message to " + email)
    except Exception as e:
        logging.exception("Failed to connect to the email server: " + str(e))
    finally:
        server.quit()


# Эта функция отправляет уведомление о возникших ошибках на
# технические контакты, указанные в конфигурации.
def send_tech_data_emails(exception):
    from core.configuration import config
    email_conf = config['email']

    subject = "some issues with run, please fix it!"
    body = str(exception) + """\

Best regards, Marchit team
"""

    send_email(subject, body, email_conf['tech-contacts'], email_conf)


# Эта функция отправляет отчет о успешно обработанных и неудачных файлах
# на контакты, указанные в конфигурации.
def send_emails(processed, errors):
    from core.configuration import config
    email_conf = config['email']

    subject = "March IT. Processed " + str(len(processed) + len(errors)) + " files"

    processed_ = '\n'.join(processed)
    errors_ = '\n'.join(errors)

    succesed_message = ("List of successfully processed files: \n" + processed_ if processed else '')
    failed_message = ("List of failed files:\n" + errors_ if errors else '')

    body = succesed_message + "\n" + failed_message + """\

Best regards,
March IT team
"""

    send_email(subject, body, email_conf['contacts'], email_conf)

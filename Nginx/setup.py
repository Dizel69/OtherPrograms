import os
import subprocess

# Настройка переменных
domain_name = "your_domain_name.com"

# Получение пути к текущему скрипту
script_dir = os.path.dirname(os.path.abspath(__file__))

# Генерация путей
nginx_config_path = os.path.join(script_dir, f"{domain_name}.conf")
webroot_path = os.path.join(script_dir, "webroot")

# Запрос электронной почты
while True:
    email = input("Введите электронную почту для получения сертификатов: ")
    if email:
        break
    else:
        print("Введите корректный электронный адрес.")


# Создание конфигурации Nginx
nginx_config = f"""
server {{
    listen 80;
    server_name {domain_name};

    location / {{
        return 301 https://{domain_name}$request_uri;
    }}
}}

server {{
    listen 443 ssl;
    server_name {domain_name};

    ssl_certificate /etc/letsencrypt/live/{domain_name}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain_name}/privkey.pem;

    location / {{
        # Proxy to your application
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}
}}
"""

# Создание папок
os.makedirs(webroot_path, exist_ok=True)

# Сохранение конфигурации Nginx
with open(nginx_config_path, "w") as f:
    f.write(nginx_config)

# Активация конфигурации Nginx
os.system("sudo nginx -t && sudo nginx -s reload")

# Получение SSL-сертификата с помощью Certbot
os.system(f"sudo certbot certonly --webroot -w {webroot_path} -d {domain_name} -m {email}")

# Автоматическое обновление сертификата
cron_job = f"0 0 */7 * * sudo certbot renew >> /var/log/certbot-renewal.log"
with open("/etc/crontab", "a") as f:
    f.write(cron_job + "\n")

print("Настройка веб-сервера Nginx и выпуск SSL-сертификатов завершены.")

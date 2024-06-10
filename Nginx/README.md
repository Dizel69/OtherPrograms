Этот скрипт автоматически развертывает Nginx и настраивает SSL-сертификаты с использованием Certbot в Docker.

## Переменные окружения

| Переменная               | Описание                                    | Значение по умолчанию                 |
|--------------------------|---------------------------------------------|---------------------------------------|
| `HOST`                   | Доменное имя для Nginx и Certbot            | `Ваш домен`                           |
| `HTTP_PORT`              | Порт для HTTP                               | `Ваш порт`                            |
| `HTTPS_PORT`             | Порт для HTTPS                              | `443`                                 |
| `NGINX_CONTAINER_NAME`   | Имя контейнера для Nginx                    | `nginx`                               |
| `CERTBOT_CONTAINER_NAME` | Имя контейнера для Certbot                  | `certbot`                             |
| `EMAIL`                  | Адрес электронной почты для Certbot         | `Ваш email`                           |

## Использование

1. Убедитесь, что Docker установлен и работает:
   ```sh
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io -y

2. Установите Docker Compose:
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose

3. Проверьте установку Docker Compose:
   docker-compose --version

4. Создайте рабочую директорию, например ~/nginx_certbot:
   mkdir ~/nginx_certbot
   cd ~/nginx_certbot

5. Запустите скрипт, он автоматически создаст папки внутри директории:
   sudo pythin3 setup.py

6. Сертификат будет лежать в папке:
   /etc/letsencrypt
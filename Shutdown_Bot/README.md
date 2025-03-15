# Telegram Shutdown Bot
## Этот проект представляет собой простого Telegram-бота, который позволяет выключать ваш компьютер с Ubuntu 24.04 через Telegram.

### Шаги по установке и настройке
1. Клонирование репозитория
```
    git clone https://github.com/yourusername/telegram-shutdown-bot.git
```

2. Создание виртуальной среды
    Для работы с проектом рекомендуется создать виртуальную среду, чтобы изолировать зависимости:
```
    cd telegram-shutdown-bot
    
    python3 -m venv myenv
    
    source myenv/bin/activate
```

3. Установка зависимостей
    Установите необходимые библиотеки для работы бота:
```
    pip install python-telegram-bot
    pip install psutil
    pip install time
    pip install platform
```

4. Настройка бота
    Получение токена Telegram:

    1. Создайте бота через BotFather в Telegram.
    2. Сохраните токен, который вы получите после создания бота.
    3. Редактирование скрипта:

        Откройте файл shutdown_bot.py и вставьте ваш токен в код

        BOT_TOKEN = 'ваш_токен'

5. Настройка автозапуска через ` systemd `
    Чтобы бот автоматически запускался при старте системы:
    1. Откройте терминал и создайте новый ` systemd ` сервис:
    ```
        sudo nano /etc/systemd/system/shutdown-bot.service
    ```

    2. Вставьте следующее содержимое в файл:
    ```
        
        [Unit]
        
        Description=Telegram бот для выключения системы
        
        After=network.target

        [Service]
        
        User=Имя_пользователя
        
        WorkingDirectory=/home/Имя_пользователя/telegram-shutdown-bot
        
        ExecStart=/home/Имя_пользователя/telegram-shutdown-bot/myenv/bin/python /home/Имя_пользователя/telegram-shutdown-bot/shutdown_bot.py
        
        Restart=always

        [Install]
        
        WantedBy=multi-user.target
    ```

    3. Сохраните файл и закройте редактор (Ctrl + X, затем Y и Enter).

    4. Перезагрузите systemd и запустите бот:
    ```
        sudo systemctl daemon-reload
        
        sudo systemctl enable shutdown-bot.service
        
        sudo systemctl start shutdown-bot.service
    ```

6. Разрешение команд без пароля
    
    1. Откройте файл sudoers:
    ```
        sudo visudo
    ```
    2. В конце файла добаьте строчку:
    ```
        Имя_пользователя ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/poweroff, /sbin/reboot
    ```

    3. Сохраните изменения.
    
7. Тестирование бота
    1. Откройте Telegram и найдите своего бота.
    2. Отправьте команду ` /shutdown `, и бот выключит систему.

8. Установка утилит для скриншота
   ```
    sudo apt update
    sudo apt install imagemagick
    sudo apt install scrot
    sudo apt install x11-apps
    ```

### Полезные команды
1. Просмотр статуса сервиса:
    ```
    sudo systemctl status shutdown-bot.service
    ```
2. Остановка и перезапуск сервиса:
    ```
    sudo systemctl stop shutdown-bot.service
    
    sudo systemctl restart shutdown-bot.service
    ```
    
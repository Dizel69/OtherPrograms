# В этом проекте я проктикуюсь в `bash`

` cleanup.sh ` - автоматическое удаление файлов старше 30 дней в директории;

` port_bot.sh ` - бот для проверки изменений в портах;

` resource_guardian.sh ` - скрипт автоматического обнаружения аномального потребления ресурсов в Linux;

` ping.sh ` - проверяет доступность сервера;

` analyze_logs.sh ` - анализ логов скрипта *ping.sh*;

` backup.sh ` - архивация директории с сохранением в другую;

` cleanup_old_files.sh ` - удаление файлов старше трёх дней;
Рекомендуется добавить в crontab:
```cron
11 11 * * * /path/to/cleanup_old_files.sh
```

` monitoring_cpu.sh ` - поиск процессов, которые потребляют >90% CPU;

` monitoring_mem.sh ` - поиск процессов, которые потребляют >60% ОЗУ;

` monitoring_cpu_and_mem.sh ` - поиск процессов, которые потребляют >90% CPU и >60% ОЗУ;

` login-track.sh ` - сбор и сохранение статистики входов пользователей;

` SSH_guard.sh ` - fаализ неудачных SSH-попыток и вывод ТОП-10 IP-адресов;

` system_inspector.sh ` - сбор подробной информации о системе;

` delete_cert-manager.sh ` - полное удаление cert-manager из k8s/k3s;

` backapp_db.sh ` - дамп базы данных PostgreSQL;

` multi_backapp_db ` - дамп баз данных PostgreSQL;

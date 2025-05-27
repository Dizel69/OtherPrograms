import socket
import time
import requests

# Параметры «вшиты» прямо в код, необходимо заменить под себя
TARGET_HOST   = ""                # общий IP на Proxmox и ВМ
TARGET_PORT   = 22                # порт, проброшенный на вашу ВМ
PING_INTERVAL = 300               # интервал между проверками (сек)
BOT_TOKEN     = ""                # токен бота
CHAT_IDS      = [""]              # ID чата

def is_host_reachable(host: str, port: int, timeout: float = 2.0) -> bool:
    """Проверяем возможность TCP-соединения с host:port."""
    try:
        with socket.create_connection((host, port), timeout):
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] TCP {host}:{port} — OK", flush=True)
            return True
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] TCP {host}:{port} — FAIL ({e})", flush=True)
        return False

def notify(chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {'chat_id': chat_id, 'text': text}
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] sent to {chat_id}: {text}", flush=True)
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR sending to {chat_id}: {e}", flush=True)

def notify_unreachable():
    for cid in CHAT_IDS:
        notify(cid, f"⚠️ Сервер недоступен!!!")

def notify_reachable():
    for cid in CHAT_IDS:
        notify(cid, f"✅ Сервер вновь доступен.")

def main():
    was_reachable = True
    while True:
        reachable = is_host_reachable(TARGET_HOST, TARGET_PORT)
        if not reachable and was_reachable:
            notify_unreachable()
        elif reachable and not was_reachable:
            notify_reachable()
        was_reachable = reachable
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()

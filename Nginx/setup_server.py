import os
import subprocess

# Загрузка переменных среды
HOST = os.getenv("HOST", "localhost")
HTTP_PORT = os.getenv("HTTP_PORT", "80")
HTTPS_PORT = os.getenv("HTTPS_PORT", "443")
NGINX_CONTAINER_NAME = os.getenv("NGINX_CONTAINER_NAME", "nginx")
CERTBOT_CONTAINER_NAME = os.getenv("CERTBOT_CONTAINER_NAME", "certbot")
EMAIL = os.getenv("EMAIL", "our_email@example.com")

def create_docker_compose():
    compose_content = f"""
    version: '3'

    services:
      nginx:
        image: nginx:latest
        container_name: {NGINX_CONTAINER_NAME}
        volumes:
          - ./nginx.conf:/etc/nginx/nginx.conf:ro
          - ./html:/usr/share/nginx/html
          - ./certbot/conf:/etc/letsencrypt
          - ./certbot/www:/var/www/certbot
        ports:
          - "{HTTP_PORT}:80"
          - "{HTTPS_PORT}:443"
        depends_on:
          - certbot

      certbot:
        image: certbot/certbot
        container_name: {CERTBOT_CONTAINER_NAME}
        volumes:
          - ./certbot/conf:/etc/letsencrypt
          - ./certbot/www:/var/www/certbot
        entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $!; done;'"
    """
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)


def create_nginx_conf():
    nginx_conf_content = f"""
    events {{}}

    http {{
        server {{
            listen 80;
            server_name {HOST};

            location / {{
                root /usr/share/nginx/html;
            }}

            location /.well-known/acme-challenge/ {{
                root /var/www/certbot;
            }}
        }}

        server {{
            listen 443 ssl;
            server_name {HOST};

            ssl_certificate /etc/letsencrypt/live/{HOST}/fullchain.pem;
            ssl_certificate_key /etc/letsencrypt/live/{HOST}/privkey.pem;

            location / {{
                root /usr/share/nginx/html;
            }}
        }}
    }}
    """
    with open("nginx.conf", "w") as f:
        f.write(nginx_conf_content)


def create_directories():
    os.makedirs("./html", exist_ok=True)
    os.makedirs("./certbot/conf", exist_ok=True)
    os.makedirs("./certbot/www", exist_ok=True)


def run_docker_compose():
    subprocess.run(["docker-compose", "up", "-d"], check=True)


def obtain_certificates():
    subprocess.run(
        [
            "docker-compose",
            "run",
            "--rm",
            "certbot",
            "certonly",
            "--webroot",
            "--webroot-path=/var/www/certbot",
            "-d",
            HOST,
            "--email",
            EMAIL,
            "--agree-tos",
            "--no-eff-email",
        ],
        check=True,
    )


def restart_nginx():
    subprocess.run(["docker-compose", "restart", "nginx"], check=True)


create_docker_compose()
create_nginx_conf()
create_directories()
run_docker_compose()
obtain_certificates()
restart_nginx()
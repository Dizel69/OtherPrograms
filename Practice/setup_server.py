import os
import subprocess

def create_docker_compose():
    compose_content = '''
    version: '3'

    services:
      nginx:
        image: nginx:latest
        container_name: nginx
        volumes:
          - ./nginx.conf:/etc/nginx/nginx.conf:ro
          - ./html:/usr/share/nginx/html
          - ./certbot/conf:/etc/letsencrypt
          - ./certbot/www:/var/www/certbot
        ports:
          - "80:80"
          - "443:443"
        depends_on:
          - certbot

      certbot:
        image: certbot/certbot
        container_name: certbot
        volumes:
          - ./certbot/conf:/etc/letsencrypt
          - ./certbot/www:/var/www/certbot
        entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $!; done;'"
    '''
    with open('docker-compose.yml', 'w') as f:
        f.write(compose_content)

def create_nginx_conf():
    nginx_conf_content = '''
    events {}

    http {
        server {
            listen 80;
            server_name localhost;

            location / {
                root /usr/share/nginx/html;
            }

            location /.well-known/acme-challenge/ {
                root /var/www/certbot;
            }
        }

        server {
            listen 443 ssl;
            server_name localhost;

            ssl_certificate /etc/letsencrypt/live/localhost/fullchain.pem;
            ssl_certificate_key /etc/letsencrypt/live/localhost/privkey.pem;

            location / {
                root /usr/share/nginx/html;
            }
        }
    }
    '''
    with open('nginx.conf', 'w') as f:
        f.write(nginx_conf_content)

def create_directories():
    os.makedirs('./html', exist_ok=True)
    os.makedirs('./certbot/conf', exist_ok=True)
    os.makedirs('./certbot/www', exist_ok=True)

def run_docker_compose():
    subprocess.run(['docker-compose', 'up', '-d'], check=True)

def obtain_certificates():
    subprocess.run([
        'docker-compose', 'run', '--rm', 'certbot', 'certonly', '--webroot',
        '--webroot-path=/var/www/certbot', '-d', 'localhost', '--email', 'your_email@example.com',
        '--agree-tos', '--no-eff-email'
    ], check=True)

def restart_nginx():
    subprocess.run(['docker-compose', 'restart', 'nginx'], check=True)

create_docker_compose()
create_nginx_conf()
create_directories()
run_docker_compose()
obtain_certificates()
restart_nginx()
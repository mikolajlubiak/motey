# Motey

## Showcase: [https://diode.zone/w/aXNYaER47MnTu8uw4LZSFW](https://diode.zone/w/aXNYaER47MnTu8uw4LZSFW)

## Running web server

Create .env file from template:
```shell
cp .env.dist .env
```
Replace default variables with your own

Start database with docker/podman compose:
```shell
sudo docker-compose up -d
```

Install all required packages (virtual environment usage is recommended):
```shell
# recommended to run before pip install
virtualenv .venv
source .venv/bin/activate
# pip install is required
pip install -r requirements.txt
pip install --upgrade setuptools
```

Initialize database:
```shell
./alembic.sh
```

Start web server:
```shell
nohup ./gunicorn.sh > ./gunicorn.log 2>&1 &
sudo caddy start --config ./Caddyfile # Change moteybot.com to your domain
```

Start Discord bot:
```shell
nohup ./bot.sh > ./bot.log 2>&1 &
```

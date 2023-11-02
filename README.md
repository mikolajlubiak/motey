# Motey

## Showcase: [https://diode.zone/w/aXNYaER47MnTu8uw4LZSFW](https://diode.zone/w/aXNYaER47MnTu8uw4LZSFW)

## Running web server

First of all, create the .env file:
```shell
cp .env.dist .env
```
And replace default parameters with your own configuration

Start database with docker compose (add `-d` flag to run as daemon - in background):
```shell
docker compose up
```

Install all required packages (virtual environment usage recommended):
```shell
# recommended
virtualenv .venv
source .venv/bin/activate
# required
pip install -r requirements.txt
```

(Optional) Set FOREIGN_KEY_CHECKS to 0 (need because otherwise the database wouldn't want to drop tables because of foreign keys):
```shell
./foreign_key_checks.sh
```

Initialize database (note: if "motey" database already exists, this will drop all existing tables):
```shell
./init_database.sh
```

Now you can start HTTP server (add `&` to run in background):
```shell
./run.sh
```

And / or Discord bot (add `&` to run in background):
```shell
./bot.sh
```

# Motey monorepo

## Running web server

First of all, create the .env file:
```shell
cp .env.dist .env
```
And replace default parameters with your own configuration

Install all required packages (virtual environment usage recommended):
```shell
pip install -r requirements.txt
```

Start database with docker compose:
```shell
docker-compose up
```

Initialize database (note: if "motey" database already exists, this will drop all existing tables):
```shell
./init_database.sh
```

Now you can start HTTP server:
```shell
./run.sh
```
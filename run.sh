#!/bin/bash

# Database
sudo docker-compose up -d

# Web server
source .venv/bin/activate
nohup ./gunicorn.sh > ./gunicorn.log 2>&1 &
sudo caddy start --config ./Caddyfile

# Bot
nohup ./bot.sh > ./bot.log 2>&1 &


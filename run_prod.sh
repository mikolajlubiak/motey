#!/bin/bash

# Database
sudo docker-compose up -d
sleep 1 # Wait for the database to launch inside the container

# Web server
source .venv/bin/activate
nohup ./gunicorn.sh > ./gunicorn.log 2>&1 &
sudo caddy start --config ./Caddyfile

# Bot
nohup ./bot.sh > ./bot.log 2>&1 &


#!/bin/bash

# Database
sudo docker-compose up -d
sleep 1 # Wait for the database to launch inside the container

# Web server
source .venv/bin/activate
nohup ./website_local.sh > ./website_local.log 2>&1 &

# Bot
nohup ./bot.sh > ./bot.log 2>&1 &


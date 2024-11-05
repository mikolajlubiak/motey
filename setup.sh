#!/bin/bash

# Python enviroment
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade setuptools

# Database
sudo docker-compose up -d
sleep 1 # Wait for the database to launch inside the container
./alembic.sh

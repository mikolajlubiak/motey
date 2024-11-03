#!/bin/bash

# Python enviroment
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade setuptools

# Database
sudo docker-compose up -d
./alembic.sh

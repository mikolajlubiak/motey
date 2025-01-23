#!/bin/bash

docker volume ls | grep motey_db_data && (docker volume rm motey_db_data || (echo "Please stop and remove the currently running motey container and run the script again."; exit))

# Python enviroment
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade setuptools

# Database
sudo docker-compose up -d

success=0
try=0

while [ $success = 0 ]; do
    try=$(($try+1))
    ./alembic.sh >> logs/alembic.out 2>> logs/alembic.err && success=1

    if [ $success = 0 ]; then
        if (($try > 9)); then
            success=2
            echo "10 failed attempts at connecting to the database, aborting."
        else
            echo "Connecting to the database was unsuccessful, retrying in 1 second. Current attempt: ${try}"
            sleep 1
        fi
    fi

    if [ $success = 1 ]; then
        echo "Connecting to the database was successful!"
    fi
done

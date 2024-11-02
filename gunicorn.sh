#!/bin/bash

set -o allexport
source .env
set +o allexport

source .venv/bin/activate

gunicorn -w 4 'motey.api.server:prepare_app()' --worker-class aiohttp.GunicornWebWorker


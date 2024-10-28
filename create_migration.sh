#!/bin/bash

set -o allexport
source .env
set +o allexport

source .venv/bin/activate

alembic revision --autogenerate -m "$1"


#!/bin/bash

set -o allexport
source .env
set +o allexport

source .venv/bin/activate

alembic upgrade head


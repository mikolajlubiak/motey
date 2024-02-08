#!/bin/bash

set -o allexport
source .env
set +o allexport

source .venv/bin/activate

python -m motey.discord.bot

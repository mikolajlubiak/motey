#!/bin/bash

set -o allexport
source .env
set +o allexport

python -m motey.discord.bot
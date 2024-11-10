#!/bin/bash

sync=false

for arg in "$@"; do
  if [[ $arg == "--sync" || $arg == "-s" ]]; then
    sync=true
  fi
done

set -o allexport
source .env
set +o allexport

source .venv/bin/activate

if $sync; then
    python -m motey.discord.bot_sync
else
    python -m motey.discord.bot
fi

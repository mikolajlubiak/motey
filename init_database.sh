#!/bin/bash

set -o allexport
source .env
set +o allexport

python -m motey.database.init_db
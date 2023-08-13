#!/bin/bash

set -o allexport
source .env
set +o allexport

docker exec -i motey-db-1 sh -c "exec mariadb -uroot -p$MYSQL_ROOT_PASSWORD -e 'SET GLOBAL FOREIGN_KEY_CHECKS = 0;'"

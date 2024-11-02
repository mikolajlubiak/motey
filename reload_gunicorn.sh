#!/bin/sh

ps aux | grep gunicorn | grep motey | awk '{ print $2 }' | xargs kill -HUP


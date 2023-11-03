#!/bin/sh

ps aux | grep gunicorn | grep lesson4future | awk '{ print $2 }' | xargs kill -HUP


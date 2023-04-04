#!/bin/ash

if [ ! -f "$CONFIG_FILE_LOCATION" ]; then
    cp /app/example/config/yt-dlp.conf $CONFIG_FILE_LOCATION
fi

gunicorn -b 0.0.0.0:5000 -w 1 main:app -k gevent
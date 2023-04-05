#!/bin/ash
exec gunicorn -b 0.0.0.0:5000 -w 1 'ytdlp_frontend:create_app()' -k gevent
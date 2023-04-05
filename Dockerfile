FROM python:3.10.10-alpine3.17

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN apk add yt-dlp ffmpeg

RUN mkdir -p /app/config

ENV VIDEOS_ROOT_FOLDER=/app/downloads \
    CONFIG_FILE_LOCATION=/app/config/yt-dlp.conf

VOLUME ["/app/downloads", "/app/config"]

CMD ["sh", "start.sh"]

EXPOSE 5000
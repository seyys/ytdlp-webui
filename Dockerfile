FROM python:3.10.10-alpine3.17

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN apk add yt-dlp

RUN mkdir -p /app/static \
&& mkdir -p /app/templates \ 
&& mkdir -p /app/example/config

COPY start.sh /app
COPY templates/* /app/templates
COPY static/* /app/static
COPY src/* /app
COPY config/* /app/example/config

ENV VIDEOS_ROOT_FOLDER=/app/downloads \
    CONFIG_FILE_LOCATION=/app/config/yt-dlp.conf

VOLUME ["/app/downloads", "/app/config"]

CMD ["sh", "/app/start.sh"]

EXPOSE 5000
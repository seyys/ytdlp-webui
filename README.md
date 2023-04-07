# Web UI for self-hosted yt-dlp

A simple web UI for downloading videos on a remote PC such as a NAS.

## Screenshot

![screenshot](https://user-images.githubusercontent.com/115355216/230538687-a947e6f6-2d27-4e51-afb6-17d3e799ca4a.png)

## Usage

### Docker Compose

```yaml
version: "3.0"
services:
  ytdlp-webui:
    image: ghcr.io/seyys/ytdlp-selfhosted-webui:master
    container_name: ytdlp-webui
    restart: "unless-stopped"
    volumes:
      - <DOWNLOADS>:/app/downloads
    ports:
      - 5000:5000
    depends_on:
      - redis
    links:
      - redis

  redis:
    image: redis:alpine
    restart: "unless-stopped"
    hostname: redis

  celery_worker:
    image: ghcr.io/seyys/ytdlp-selfhosted-webui:master
    command: ["celery", "-A", "make_celery", "worker", "--loglevel", "INFO"]
    depends_on:
      - redis
    restart: "unless-stopped"
    environment:
      - FILENAME_TEMPLATE=%(title)s - [%(id)s].mkv
      - CHMOD=<PERMS> # optional
      - CHOWN_UID=<UID> # optional
      - CHOWN_GID=<GID> # optional
    volumes:
      - <DOWNLOADS>:/app/downloads
      - <CONFIG>:/app/config
    links:
      - redis
```

### Configuration

Edit `yt-dlp.conf` in the `<CONFIG>` directory. Refer to the [yt-dlp options](https://github.com/yt-dlp/yt-dlp#usage-and-options).

## Running locally

Clone this repo, install pip requirements, then run

```bash
redis-server & REDIS_URL=redis://localhost celery -A make_celery worker --loglevel INFO & REDIS_URL=redis://localhost flask --app ytdlp_frontend run
```

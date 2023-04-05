from ytdlp_frontend import create_app
import os
import shutil


if not os.environ["CONFIG_FILE_LOCATION"] in os.listdir():
    shutil.copy("/app/ytdlp_frontend/config/yt-dlp.conf", os.environ["CONFIG_FILE_LOCATION"])
flask_app = create_app()
celery_app = flask_app.extensions["celery"]

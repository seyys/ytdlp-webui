from ytdlp_frontend import create_app
import os
import shutil

config_location = os.environ.get("CONFIG_FILE_LOCATION", "./ytdlp_frontend/config/yt-dlp.conf")
if not os.path.exists(config_location):
    shutil.copy("./ytdlp_frontend/config/yt-dlp.conf", config_location)
flask_app = create_app()
celery_app = flask_app.extensions["celery"]

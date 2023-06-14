import subprocess
import os
from celery import shared_task, Task
from typing import List
from glob import glob


init = r"""
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
            <title>yt-dlp frontend</title>
            <meta name="viewport" content="width=device-width, initial-scale=1" />
        </head>
        <body>
    """


class Message:
    message: List[str]
    progress: float


@shared_task(bind=True, ignore_result=False)
def ytdlp(self: Task, url, directory) -> object:
    msg: List[str] = []

    chmod = int(os.environ.get("CHMOD", "-1"), 8)  # chmod is in octal
    chown_uid = int(os.environ.get("CHOWN_UID", -1))
    chown_gid = int(os.environ.get("CHOWN_GID", -1))

    filedirectory = os.path.join(os.environ.get("VIDEOS_ROOT_FOLDER", "./"), directory)

    if directory not in os.listdir(os.environ.get("VIDEOS_ROOT_FOLDER", "./")):
        os.makedirs(filedirectory)
        os.chmod(filedirectory, chmod)
        os.chown(filedirectory, chown_uid, chown_gid)

    filetemplate = os.environ.get("FILENAME_TEMPLATE", "%(title)s - %(id)s.mkv")
    filename = (
        subprocess.run(
            f'yt-dlp "{url}" -o "{filetemplate}" --get-filename',
            shell=True,
            stdout=subprocess.PIPE,
        )
        .stdout.decode("utf-8")
        .strip()
    )
    filepath = os.path.join(filedirectory, filename)
    cmd = f'yt-dlp {url} -o "{filepath}" --config-location "{os.environ.get("CONFIG_FILE_LOCATION", "./ytdlp_frontend/config/yt-dlp.conf")}"'
    with subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True
    ) as p:
        if p.stdout == None:
            return
        for line in p.stdout:
            msg.append(line)
            self.update_state(state="PROGRESS", meta={"filename": filename, "message": msg})
    self.update_state(state="PROGRESS", meta={"filename": filename, "message": msg})

    if chmod != -1:
        [
            os.chmod(os.path.join(filedirectory, f), chmod)
            for f in os.listdir(filedirectory)
            if f.startswith(".".join(filename.split(".")[:-1]))
        ]
        msg.append(f"chmod {oct(chmod).replace('0o','')}\n") # chmod is in octal
        self.update_state(state="PROGRESS", meta={"filename": filename, "message": msg})
    if chown_uid >= 0 and chown_gid >= 0:
        [
            os.chown(os.path.join(filedirectory, f), chown_uid, chown_gid)
            for f in os.listdir(filedirectory)
            if f.startswith(".".join(filename.split(".")[:-1]))
        ]
        msg.append(f"chown {chown_uid}:{chown_gid}\n")
        self.update_state(state="PROGRESS", meta={"filename": filename, "message": msg})
    return {"filename": filename, "message": msg}

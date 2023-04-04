import subprocess
import os


init = r"""
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
            <title>yt-dlp frontend</title>
            <meta name="viewport" content="width=device-width, initial-scale=1" />
        </head>
        <body>
    """


def ytdlp(url, directory):
    yield (init)
    filetemplate = os.environ.get("FILENAME_TEMPLATE", "%(title)s - %(id)s.mkv") #%(title)s - %(id)s.mkv
    filename = (
        subprocess.run(
            f'yt-dlp {url} -o "{filetemplate}" --get-filename',
            shell=True,
            stdout=subprocess.PIPE,
        )
        .stdout.decode("utf-8")
        .strip()
    )
    filepath = os.path.join(os.environ.get("VIDEOS_ROOT_FOLDER", "./"), directory, filename)
    cmd = f'yt-dlp {url} -o "{filepath}" --config-location "{os.environ.get("CONFIG_FILE_LOCATION", "./yt-dlp.conf")}"'
    yield (f"<strong>{cmd}</strong>")
    yield (f'<div class="stdout">')
    with subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True
    ) as p:
        if p.stdout == None:
            return "Error"
        for line in p.stdout:
            yield (line + "<br/>")
        yield ("-------DONE-------")
        yield ("</div>")

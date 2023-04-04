from flask import Flask, render_template, request, stream_with_context
import os
from ytdlp import ytdlp


app = Flask(__name__)

url_field_name = "url"
dir_field_name = "dir"


@app.route("/")
def index():
    lsdir = [d for d in next(os.walk(os.environ.get("VIDEOS_ROOT_FOLDER", "./")))[1]]
    context = {
        "url_field_name": url_field_name,
        "dir_field_name": dir_field_name,
        "lsdir": lsdir,
    }
    return render_template("index.html", context=context)


@app.post("/submit")
def submit():
    print(request)
    url = request.form[url_field_name]
    directory = request.form[dir_field_name]
    if directory == "":
        return "Please enter a directory"
    if directory not in os.listdir(os.environ.get("VIDEOS_ROOT_FOLDER", "./")):
        os.makedirs(directory)
    return stream_with_context(ytdlp(url, directory))
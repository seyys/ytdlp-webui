from flask import Flask, render_template
from celery import Celery, Task
import os


url_field_name = "url"
dir_field_name = "dir"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis",
            result_backend="redis://redis",
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)


    @app.route("/")
    def index():
        lsdir = [d for d in next(os.walk(os.environ.get("VIDEOS_ROOT_FOLDER", "./")))[1]]
        context = {
            "url_field_name": url_field_name,
            "dir_field_name": dir_field_name,
            "lsdir": lsdir,
        }
        return render_template("index.html", context=context)

    from . import views

    app.register_blueprint(views.bp)
    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

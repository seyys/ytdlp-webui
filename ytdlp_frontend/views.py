from celery.result import AsyncResult
from flask import Blueprint, request
from . import url_field_name, dir_field_name, tasks

bp = Blueprint("task", __name__, url_prefix="/task")


@bp.get("/result/<id>")
def result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    ready = result.ready()
    return {
        "ready": ready,
        "successful": result.successful() if ready else None,
        "value": result.get() if ready else result.result,
    }


@bp.post("/submit")
def submit_post() -> dict[str, object]:
    url = request.form.get(url_field_name)
    directory = request.form.get(dir_field_name, '')
    result = tasks.ytdlp.delay(url=url, directory=directory)
    return {"result_id": result.id}

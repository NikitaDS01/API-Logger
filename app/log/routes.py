import time
import logging
import tempfile
import os

from flask import Response, abort, request, jsonify
from pydantic import ValidationError

from app.models.project import Project
from app.models.log import Log
from app.log.schema import LogSchema
from app.extensions import db
from app.bot import bot
from app.log import bp 
from config import general_cfg


@bp.post("")
def create_log():
    try:
        log_info = LogSchema(**request.get_json())
        if log_info.ts_create is None:
            log_info.ts_create = time.time()
    except ValidationError as e:
        abort(400, f"Wrong body format. {e.errors()}")
    
    project: Project = Project.query.get_or_404(log_info.project)
    log_info.project = project.name

    send_log_file(project.name,log_info)
    send_log_db(log_info, project)
    if log_info.level >= project.log_level:
        send_log_bot(log_info, project)
    return Response(status=201)

@bp.get("")
def get_logs():
    logs: list[Log] = Log.query.all()
    response = []
    for log in logs:
        log_info = LogSchema(
            level=log.level,
            project=log.project_id,
            message=log.message,
            ts_create=log.ts_create
        )
        response.append(log_info.model_dump())
    return jsonify(response)

# Send log in file
def send_log_file(project_name:str,log_info: LogSchema):
    logger = logging.getLogger(project_name)
    message_log = str.format(
        "[{project}]\t{message}",
        project=project_name,
        message=log_info.message
    )
    logger.log(log_info.level, message_log)

# Send log in database
def send_log_db(log_info: LogSchema, project: Project):
    log: Log = Log(
        level = log_info.level,
        ts_create = log_info.ts_create,
        message = log_info.message,
        project_id = project.id
    )
    db.session.add(log)
    db.session.commit()

def send_log_bot(log_info: LogSchema, project: Project):
    # Send log in telegram bot
    message_bot = str.format(
        "Log level: <b>{level}</b>\nProject: {project}",
        level=logging.getLevelName(log_info.level),
        project=log_info.project,
    )

    logs: list[Log] = Log.query.filter_by(project_id=project.id).\
        order_by(Log.ts_create.desc()).limit(general_cfg["count_last_message"]).all()

    file_name = time.strftime('%d:%m:%Y,%H:%M:%S', time.gmtime(log_info.ts_create)) + '.txt'
    with tempfile.NamedTemporaryFile() as file:
        for log in logs:
            log_text = str.format(
                "Time created: {ts}\tLog level: {level}\tProject: {project}\t{text}\n",
                ts=time.strftime('%d:%m:%Y,%H:%M:%S', time.gmtime(log.ts_create)),
                level=logging.getLevelName(log_info.level),
                project=log.project_id,
                text=log.message,
            )
            file.write(str.encode(log_text))
        file.seek(0)
        bot.send_document(
            message=message_bot,
            file_name=file_name,
            document=file,
        )

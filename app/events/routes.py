import time
import logging
import os

from flask import Response, abort, request, jsonify
from pydantic import ValidationError

from app.models.project import Project
from app.models.event import Event
from app.events.schema import EventSchema
from app.extensions import db
from app.events import bp 
from app.bot import bot


@bp.post("")
def create_log():
    try:
        event_info = EventSchema(**request.get_json())
        if event_info.ts_create is None:
            event_info.ts_create = time.time()
    except ValidationError as e:
        abort(400, f"Wrong body format. {e.errors()}")
    
    project: Project = Project.query.get_or_404(event_info.project)
    event_info.project = project.name

    # Send log in database
    event: Event = Event(
        type = event_info.type,
        ts_create = event_info.ts_create,
        message = event_info.message,
        project_id = project.id
    )
    db.session.add(event)
    db.session.commit()

    # Send log in telegram bot
    message = str.format(
        "Event type: <b>{type}</b>\nProject: {project}\nMessage: {text}",
        type=event_info.type,
        project=event_info.project,
        text=event_info.message,
    )
    bot.send_message(message)

    return Response(status=201)

@bp.get("")
def get_logs():
    events: list[Event] = Event.query.all()
    response = []
    for event in events:
        event_info = EventSchema(
            type=event.type,
            project=event.project_id,
            message=event.message,
            ts_create=event.ts_create
        )
        response.append(event_info.model_dump())
    return jsonify(response)
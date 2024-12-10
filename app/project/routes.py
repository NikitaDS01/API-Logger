import time
import os

from flask import Response, abort, jsonify, request
from pydantic import ValidationError

from app.models.project import Project
from app.project.schema import ProjectSchema
from app.extensions import db
from app.project import bp

@bp.post("")
def create_project():
    try:
        project_info = ProjectSchema(**request.get_json())
    except ValidationError as e:
        abort(400, f"Wrong body format. {e.errors()}")

    project: Project = Project(
        id=project_info.id,
        name = project_info.name,
        ts_create = time.time(),
        log_level = project_info.log_level
    )

    dir_log = os.path.abspath(os.path.join("logs", project_info.id))
    if not os.path.exists(dir_log):
        os.mkdir(dir_log)

    db.session.add(project)
    db.session.commit()

    return jsonify({
        "id": project.id,
        "name": project.name,
        "ts_create": project.ts_create,
        "log_level": project.log_level
    })

@bp.get("")
def get_projects():
    projects: list[Project] =  Project.query.all()
    response = []
    for project in projects:
        json_data = {
            "id": project.id,
            "name": project.name,
            "ts_create": project.ts_create,
            "log_level": project.log_level
        }
        response.append(json_data)
    return jsonify(response)

@bp.get("/{string:id}")
def get_project_by_id(id: str):
    project: Project =  Project.query.get_or_404(id)
    
    return jsonify({
        "id": project.id,
        "name": project.name,
        "ts_create": project.ts_create,
        "log_level": project.log_level
    })
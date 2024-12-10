from flask import Blueprint

bp = Blueprint("event", __name__)

from app.events import routes

import os

from flask import Flask

from app.bot import bot
from app.extensions import db
from logs import logger_configure
from app.project import bp as project_bp
from app.events import bp as event_bp
from app.log import bp as log_bp


def create_app() -> Flask:
    # Set config
    logger_configure()

    # Create app object
    app = Flask(__name__)

    # Add configs at app
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(os.path.dirname(__file__), "app.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init Flask extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(project_bp, url_prefix="/project")
    app.register_blueprint(event_bp, url_prefix="/event")
    app.register_blueprint(log_bp, url_prefix="/log")

    return app

from flask_sqlalchemy import SQLAlchemy

from app.models import Base


db = SQLAlchemy(
    model_class=Base
)

import time

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.sqlite import (
    FLOAT, INTEGER, TEXT
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.project import Project
from app.extensions import db


class Event(db.Model):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    ts_create: Mapped[float] = mapped_column(FLOAT)
    type: Mapped[str] = mapped_column(TEXT)
    message: Mapped[str] = mapped_column(TEXT)
    
    project_id: Mapped[str] = mapped_column(ForeignKey(Project.id)) 
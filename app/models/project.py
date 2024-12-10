from logging import INFO

from sqlalchemy.dialects.sqlite import (
    TEXT, 
    INTEGER,
    FLOAT
)
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db


class Project(db.Model):
    __tablename__ = "project"

    id: Mapped[str] = mapped_column(TEXT, primary_key=True)
    name: Mapped[str] = mapped_column(TEXT)
    ts_create: Mapped[float] = mapped_column(FLOAT)
    log_level: Mapped[int] = mapped_column(INTEGER, default=INFO)
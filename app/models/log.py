from logging import INFO, getLevelName
import time

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.sqlite import (
    FLOAT, INTEGER, TEXT
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.project import Project
from app.extensions import db


class Log(db.Model):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    level: Mapped[int] = mapped_column(INTEGER, default=INFO)
    ts_create: Mapped[float] = mapped_column(FLOAT)
    message: Mapped[str] = mapped_column(TEXT)
    
    project_id: Mapped[str] = mapped_column(ForeignKey(Project.id)) 

    @property
    def level_name(self):
        return getLevelName(self.level)

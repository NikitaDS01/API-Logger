from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LogSchema(BaseModel):
    level: int
    project: str
    message: str
    ts_create: Optional[float] = None
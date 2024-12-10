from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventSchema(BaseModel):
    project: str
    type: str
    message: str
    ts_create: Optional[float] = None
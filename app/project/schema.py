from pydantic import BaseModel


class ProjectSchema(BaseModel):
    id: str
    name: str
    log_level: int 
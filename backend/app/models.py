from pydantic import BaseModel


class Job(BaseModel):
    id: str
    tool: str
    target: dict
    options: dict
    status: str = "queued"

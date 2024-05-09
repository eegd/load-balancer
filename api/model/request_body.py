from pydantic import BaseModel


class TaskCreate(BaseModel):
    key: str
    msg: str

from pydantic import BaseModel
from datetime import datetime

class Todo(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool = False
    is_deleted: bool = False
    updated_at: int = int(datetime.now().timestamp())
    creation: int = int(datetime.now().timestamp())
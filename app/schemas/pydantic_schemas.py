from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskRead(TaskCreate):
    id: int
    created_at: datetime

class TimerStart(BaseModel):
    task_id: int

class TimerStop(BaseModel):
    timer_id: int
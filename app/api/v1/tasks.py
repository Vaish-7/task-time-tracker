from fastapi import APIRouter, Depends, HTTPException
from app.schemas.pydantic_schemas import TaskCreate, TaskRead
from app.db.session import get_session
from sqlmodel import Session, select
from app.models.models import Task

router = APIRouter()

@router.post('/', response_model=TaskRead)
def create_task(payload: TaskCreate, session: Session = Depends(get_session)):
    task = Task(title=payload.title, description=payload.description, user_id=1)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get('/')
def list_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()


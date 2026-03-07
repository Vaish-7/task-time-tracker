from fastapi import APIRouter, Depends, HTTPException
from app.schemas.pydantic_schemas import TaskCreate, TaskRead
from app.db.session import get_session
from sqlmodel import Session, select
from app.models.models import Task

router = APIRouter()

@router.get('/')
def list_tasks(session: Session = Depends(get_session)):
    tasks =  session.exec(select(Task)).all()
    return tasks

@router.post('/')
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}")
def update_task(task_id: int, updated: Task, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated.title
    task.description = updated.description
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"delete": task_id}

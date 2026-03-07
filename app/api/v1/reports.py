from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
from app.core.session import get_session
from app.models import Task, Timer
from datetime import datetime


router = APIRouter()

def calculate_total_time_for_task(
        task_id: int,
        session: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
        ) -> dict:
    
    query = select(Timer).where(Timer.task_id == task_id).all()
    
    if start_date:
        query = query.where(Timer.start_time >= start_date)
    if end_date:
        query = query.where(Timer.end_time <= end_date)

    timers = session.exec(query).all()

    total_seconds = sum(
        (t.end_time - t.start_time).total_seconds()
        for t in timers if t.end_time
    )
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    return {
        "total_seconds": total_seconds,
        "hours": int(hours),
        "minutes": int(minutes),
        "formatted": f"{hours}h {minutes}m"
    }
    
@router.get("/task/{task_id}/total_time")
def total_time(task_id:int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code = 404, detail="Task not Found")
    
    result = calculate_total_time_for_task(task_id, session)
    return {"task_id": task_id, **result}
    

@router.get("/task/summary")
def tasks_summary(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    summary = []

    for task in tasks:
        result = calculate_total_time_for_task(task.id, session)
        summary.append(
            {
                "task_id": task.id,
                "title": task.title,
                **result
            }
        )
    return {
        "tasks": summary
    }

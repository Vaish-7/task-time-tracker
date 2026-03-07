from fastapi import APIRouter, Depends, HTTPException
from app.schemas.pydantic_schemas import TimerStart, TimerStop
from app.db.session import get_session
from sqlmodel import Session, select
from app.models.models import Timer, Task
from datetime import datetime

router = APIRouter()

@router.post("/start/{task_id}")
def start_timer(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not Found")
    
    timer = Timer(task_id=task_id, start_time=datetime.utcnow())
    session.add(timer)
    session.commit()
    session.refresh(timer)
    return timer

@router.post("/stop/{timer_id}")
def stop_timer(timer_id: int, session: Session = Depends(get_session)):
    timer = session.get(Timer, timer_id)
    if not timer or timer.end_time is not None:
        raise HTTPException(status_code=404, detail="Active timer not found")
    
    timer.end_time = datetime.utcnow()
    session.add(timer)
    session.commit()
    session.refresh(timer)
    return timer

@router.get("/duration/{timer_id}")
def get_duration(timer_id: int, session: Session = Depends(get_session)):
    timer = session.get(Timer, timer_id)
    if not timer:
       raise HTTPException(status_code=404, detail="Timer Not Found")
    if not timer.end_time:
        raise HTTPException(status_code=400, detail="Timer is still running")
    duration = (timer.end_time - timer.start_time).total_seconds()
    return {
        "timer_id": timer_id,
        "duration_seconds": duration,
        "duration_minutes": round(duration / 60, 2)
    }
    
@router.get("/task/{task_id}")
def list_timers(task_id: int, session: Session = Depends(get_session)):
    timers = session.exec(select(Timer).where(Timer.task_id == task_id)).all()
    return timers

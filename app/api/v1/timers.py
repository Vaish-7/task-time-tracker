from fastapi import APIRouter, Depends, HTTPException
from app.schemas.pydantic_schemas import TimerStart, TimerStop
from app.db.session import get_session
from sqlmodel import Session
from app.models.models import Timer
from datetime import datetime

router = APIRouter()

@router.post("/start")
def start_timer(payload: TimerStart, session: Session = Depends(get_session)):
    timer = Timer(task_id=payload.task_id, start_at=datetime.utcnow())
    session.add(timer)
    session.commit()
    session.refresh(timer)
    return {"timer_id": timer.id, "started_at": timer.start_at}

@router.post("/stop")
def stop_timer(payload: TimerStop, session: Session = Depends(get_session)):
    timer = session.get(Timer, payload.timer_id)
    if not timer or timer.end_at:
        raise HTTPException(status_code=400, detail="Invalid timer")
    timer.end_at = datetime.utcnow()
    session.add(timer)
    session.commit()
    session.refresh(timer)
    return {"timer_id": timer.id, "duration_seconds": (timer.end_at - timer.start_at).total_seconds()}

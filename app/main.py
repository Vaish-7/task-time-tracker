from fastapi import FastAPI
from app.api.v1 import auth, reports, tasks, timers
from app.db.session import init_db

app = FastAPI(title="Task Time Tracker")

@app.on_event("startup")
async def on_startup():
    init_db()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(timers.router, prefix="/api/v1/timers", tags=["timers"])

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
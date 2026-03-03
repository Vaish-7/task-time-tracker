# app/api/v1/reports.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_reports():
    # For now, just return a dummy response
    return [{"id": 1, "report": "Sample report"}]

@router.post("/")
def create_report(title: str):
    # For now, just return a dummy response
    return {"id": 2, "report": title}
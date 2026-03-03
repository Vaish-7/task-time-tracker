# app/api/v1/auth.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    # For now, just return a dummy response
    return {"message": f"Logged in as {username}"}

@router.post("/register")
def register(username: str, password: str):
    # For now, just return a dummy response
    return {"message": f"Registered user {username}"}
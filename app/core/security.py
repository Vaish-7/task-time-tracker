from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

PWD_CTX = CryptContext(schemas=["bycrypt"], deprecated="auto")
SECRET = "dev-secret-key"

def hash_password(password: str) -> str:
    return PWD_CTX.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return PWD_CTX.verify(plain, hashed)

def create_access_token(sub: str, expires_minutes: int = 60):
    payload = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, SECRET, algorithm="HS256")
import jwt
import datetime
from config import JWT_SECRET, JWT_ALGO

def create_token(payload, expires_minutes=60*24):
    p = payload.copy()
    p["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    return jwt.encode(p, JWT_SECRET, algorithm=JWT_ALGO)

def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except Exception:
        return None

from config import USERS
from passlib.hash import bcrypt
from datetime import datetime

def create_user(email, password, role="viewer", name=None):
    hashed = bcrypt.hash(password)
    user = {
        "email": email,
        "password": hashed,
        "role": role,
        "name": name,
        "created_at": datetime.utcnow()
    }
    res = USERS.insert_one(user)
    return str(res.inserted_id)

def find_by_email(email):
    return USERS.find_one({"email": email})

def get_public(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name"),
        "role": user.get("role")
    }

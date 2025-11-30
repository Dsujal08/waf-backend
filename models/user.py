# models/user.py
from config import USERS
from passlib.hash import bcrypt
from datetime import datetime

VALID_ROLES = ["admin", "user"]


def create_user(email, password, role="user", name=None):
    if role not in VALID_ROLES:
        raise ValueError("Role must be 'admin' or 'user'.")

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


def authenticate(email, password):
    """Validate login for admin/user only."""
    user = find_by_email(email)
    if not user:
        return None

    if not bcrypt.verify(password, user["password"]):
        return None

    # Must be admin/user
    if user.get("role") not in VALID_ROLES:
        return None

    return user


def get_public(user):
    """Safe user object for response/JWT."""
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name"),
        "role": user.get("role")
    }

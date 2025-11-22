from config import USERS
from passlib.hash import bcrypt, argon2
from datetime import datetime
from bson import ObjectId

# --- Option 1: Keep using bcrypt (truncate password to 72 bytes) ---
def create_user(email, password, role="viewer", name=None):
    # Truncate password to 72 bytes to avoid bcrypt limitation
    hashed = bcrypt.hash(password[:72])
    doc = {
        "email": email,
        "password": hashed,
        "role": role,
        "name": name,
        "createdAt": datetime.utcnow()
    }
    res = USERS.insert_one(doc)
    return str(res.inserted_id)

# --- Option 2: Switch to Argon2 (recommended, supports long passwords) ---
"""
def create_user(email, password, role="viewer", name=None):
    hashed = argon2.hash(password)
    doc = {
        "email": email,
        "password": hashed,
        "role": role,
        "name": name,
        "createdAt": datetime.utcnow()
    }
    res = USERS.insert_one(doc)
    return str(res.inserted_id)
"""

def find_by_email(email):
    return USERS.find_one({"email": email})

def get_public(user_doc):
    if not user_doc: 
        return None
    return {
        "id": str(user_doc["_id"]),
        "email": user_doc["email"],
        "role": user_doc.get("role"),
        "name": user_doc.get("name")
    }

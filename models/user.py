# models/user.py
from config import USERS
from passlib.hash import bcrypt
from datetime import datetime
import pytz

VALID_ROLES = ["admin", "user"]
UTC = pytz.utc


def normalize_email(email: str) -> str:
    """Convert email to lowercase to ensure unique indexing."""
    return email.strip().lower()


def create_user(email, password, role="user", name=None):
    """Create a new user securely with validation."""
    email = normalize_email(email)

    if role not in VALID_ROLES:
        raise ValueError("Role must be 'admin' or 'user'.")

    # Check for duplicates
    if USERS.find_one({"email": email}):
        raise ValueError("Email already exists.")

    hashed = bcrypt.hash(password)

    user = {
        "email": email,
        "password": hashed,
        "role": role,
        "name": name or "",

        # Store aware datetime
        "created_at": datetime.utcnow().replace(tzinfo=UTC),

        # Optional login info tracking
        "last_login_utc": None,
        "last_login_ip": None,
        "last_login_device": None,
    }

    result = USERS.insert_one(user)
    return str(result.inserted_id)


def find_by_email(email):
    email = normalize_email(email)
    return USERS.find_one({"email": email})


def authenticate(email, password):
    """Validate login only for admin/user roles."""
    user = find_by_email(email)
    if not user:
        return None

    # Password validation
    if not bcrypt.verify(password, user["password"]):
        return None

    # Role check
    if user.get("role") not in VALID_ROLES:
        return None

    return user


def update_login_info(user_id, ip=None, device_id=None):
    """Update last login metadata (optional but useful)."""
    USERS.update_one(
        {"_id": user_id},
        {
            "$set": {
                "last_login_utc": datetime.utcnow().replace(tzinfo=UTC).isoformat(),
                "last_login_ip": ip,
                "last_login_device": device_id,
            }
        }
    )


def get_public(user):
    """Return safe user object for JWT or API response."""
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name", ""),
        "role": user.get("role", "user"),
        "created_at": user.get("created_at").isoformat() if user.get("created_at") else None,
        "last_login_utc": user.get("last_login_utc"),
        "last_login_ip": user.get("last_login_ip"),
        "last_login_device": user.get("last_login_device")
    }

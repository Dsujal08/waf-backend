# models/log.py
from datetime import datetime
import pytz
from config import LOGS

VALID_ROLES = ["admin", "user"]
IST = pytz.timezone("Asia/Kolkata")


def log_request(data: dict):
    """Store a cleaned log entry with valid role in MongoDB."""

    # UTC timestamp (aware datetime)
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)

    # Convert to IST
    ist_now = utc_now.astimezone(IST)

    # Validate role
    role = data.get("role")
    if role not in VALID_ROLES:
        role = "user"  # Default safe role (never 'unknown')

    log_entry = {
        "action": data.get("action", ""),
        "email": data.get("email", ""),
        "role": role,
        "extra": data.get("extra", ""),
        "timestamp": utc_now,
        "timestamp_ist": ist_now.strftime("%d/%m/%y, %I:%M:%S %p")
    }

    LOGS.insert_one(log_entry)


def get_logs():
    """Return logs sorted by latest first."""
    return list(LOGS.find().sort("timestamp", -1))

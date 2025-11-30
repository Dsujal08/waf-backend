# models/log.py
from datetime import datetime
import pytz
from config import LOGS

VALID_ROLES = ["admin", "user"]
IST = pytz.timezone("Asia/Kolkata")


def log_request(data: dict):
    """Store complete enriched log entry in MongoDB."""

    # UTC timestamp (aware datetime)
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    ist_now = utc_now.astimezone(IST)

    # Validate role
    role = data.get("role")
    if role not in VALID_ROLES:
        role = "user"

    log_entry = {
        "action": data.get("action", ""),
        "email": data.get("email", ""),
        "role": role,

        # IP + Device + Browser
        "ip": data.get("ip", ""),
        "device_id": data.get("device_id", ""),
        "user_agent": data.get("user_agent", ""),

        # Geo Data (passed from backend/API or from client)
        "city": data.get("city", ""),
        "state": data.get("state", ""),
        "country": data.get("country", ""),

        # Login timestamps
        "login_time_utc": utc_now.isoformat(),
        "login_time_ist": ist_now.strftime("%d/%m/%y, %I:%M:%S %p"),

        # Original timestamps for sorting
        "timestamp": utc_now,
        "timestamp_ist": ist_now.strftime("%d/%m/%y, %I:%M:%S %p"),

        "extra": data.get("extra", "")
    }

    LOGS.insert_one(log_entry)


def get_logs():
    """Return all logs sorted by latest first."""
    return list(LOGS.find().sort("timestamp", -1))

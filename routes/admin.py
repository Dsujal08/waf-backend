# routes/admin_logs.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.log import get_logs
from datetime import datetime
import pytz

bp = Blueprint("logs_api", __name__, url_prefix="/api/admin/logs")
IST = pytz.timezone("Asia/Kolkata")


@bp.route("/", methods=["GET"])
@jwt_required()
def fetch_logs():
    user_id = get_jwt_identity()  # not used but verifies identity
    claims = get_jwt()

    # Only admins can view logs
    if claims.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    logs = get_logs()
    formatted_logs = []

    for log in logs:
        utc_ts = log.get("timestamp")
        dt_utc = None

        # Convert stored UTC timestamp to IST
        if utc_ts:
            if isinstance(utc_ts, datetime):
                dt_utc = utc_ts
            else:
                dt_utc = datetime.fromisoformat(str(utc_ts))

            dt_utc = dt_utc.replace(tzinfo=pytz.utc)
            dt_ist = dt_utc.astimezone(IST)
            timestamp_ist = dt_ist.strftime("%d/%m/%y, %I:%M:%S %p")
        else:
            timestamp_ist = ""

        formatted_logs.append({
            "_id": str(log["_id"]),
            "timestamp_utc": dt_utc.isoformat() if dt_utc else "",
            "timestamp_ist": timestamp_ist,

            "action": log.get("action", ""),
            "email": log.get("email", ""),
            "role": log.get("role", ""),

            "ip": log.get("ip", ""),
            "device_id": log.get("device_id", ""),
            "user_agent": log.get("user_agent", ""),

            "city": log.get("city", ""),
            "state": log.get("state", ""),
            "country": log.get("country", ""),

            "login_time_utc": log.get("login_time_utc", ""),
            "login_time_ist": log.get("login_time_ist", ""),

            "extra": log.get("extra", "")
        })

    return jsonify(formatted_logs), 200

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.log import get_logs
from datetime import datetime
import pytz

bp = Blueprint("admin_logs", __name__, url_prefix="/api/admin/logs")

IST = pytz.timezone("Asia/Kolkata")

@bp.route("/", methods=["GET"])
@jwt_required()
def fetch_logs():
    user_id = get_jwt_identity()

    claims = get_jwt()
    role = claims.get("role")

    # Only admins can view logs
    if role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    logs = get_logs()
    fixed_logs = []

    for log in logs:
        utc_ts = log.get("timestamp")
        dt_utc = None

        # Convert timestamp to IST safely
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

        fixed_logs.append({
            "_id": str(log["_id"]),
            "timestamp": dt_utc.isoformat() if dt_utc else "",
            "timestamp_ist": timestamp_ist,
            "action": log.get("action", ""),
            "email": log.get("email", ""),
            "role": log.get("role"),  # <-- ALWAYS RETURN ROLE
            "extra": log.get("extra", "")
        })

    return jsonify(fixed_logs), 200

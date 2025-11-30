from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId
from datetime import datetime
from config import USERS, LOGS

bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@bp.route("/logs", methods=["GET"])
@jwt_required()
def get_logs():
    user_id = get_jwt_identity()
    claims = get_jwt()  # contains role, email, etc.

    # Validate user exists
    try:
        user = USERS.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "Invalid user"}), 401
    except:
        return jsonify({"error": "Invalid user"}), 401

    # Only admin can access logs
    if claims.get("role") != "admin":
        return jsonify({"error": "Access denied"}), 403

    # Fetch logs
    logs_cursor = LOGS.find().sort("timestamp", -1)
    logs = [
        {
            "_id": str(log["_id"]),
            "timestamp": log.get("timestamp").isoformat() if log.get("timestamp") else None,
            "action": log.get("action", ""),
            "email": log.get("email", ""),
            "role": log.get("role", ""),   # <-- NOW WILL SHOW
            "extra": log.get("extra", "")
        }
        for log in logs_cursor
    ]

    return jsonify(logs), 200

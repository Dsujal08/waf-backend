from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId
from config import USERS, LOGS

bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@bp.route("/logs", methods=["GET"])
@jwt_required()
def get_logs():
    # JWT identity is user ID (string)
    user_id = get_jwt_identity()
    claims = get_jwt()  # get additional_claims (role/email)

    # Validate user exists
    try:
        user = USERS.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return jsonify({"error": "Invalid user"}), 401

    # Check admin role
    if not user or claims.get("role") != "admin":
        return jsonify({"error": "Access denied"}), 403

    logs_cursor = LOGS.find().sort("timestamp", -1)
    logs = [
        {
            "_id": str(log["_id"]),
            "timestamp": log["timestamp"].isoformat() if log.get("timestamp") else None,
            "action": log.get("action", ""),
            "email": log.get("email", ""),
            "role": log.get("role", ""),
            "extra": log.get("extra", "")
        }
        for log in logs_cursor
    ]

    return jsonify(logs), 200

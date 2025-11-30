from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.log import get_logs

bp = Blueprint("logs", __name__, url_prefix="/api/admin/logs")

@bp.route("/", methods=["GET"])
@jwt_required()
def fetch_logs():
    # identity usually contains only the user_id
    user_id = get_jwt_identity()

    # role is stored inside additional claims
    claims = get_jwt()
    role = claims.get("role")

    if role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    logs = get_logs()

    # Convert ObjectId to string
    for log in logs:
        log["_id"] = str(log["_id"])
        # Ensure role field exists
        log["role"] = log.get("role", "")

    return jsonify(logs), 200

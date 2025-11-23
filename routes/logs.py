from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.log import get_logs

bp = Blueprint("logs", __name__, url_prefix="/api/admin/logs")

@bp.route("/", methods=["GET"])
@jwt_required()
def fetch_logs():
    identity = get_jwt_identity()
    if identity.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    logs = get_logs()
    # Convert ObjectId to string for frontend
    for log in logs:
        log["_id"] = str(log["_id"])
    return jsonify(logs), 200

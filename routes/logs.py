from flask import Blueprint, request, jsonify
from models.log import get_logs

bp = Blueprint("logs", __name__, url_prefix="/api/logs")

@bp.route("/", methods=["GET"])
def list_logs():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 50))
    skip = page * size
    return jsonify(get_logs({}, skip=skip, limit=size))

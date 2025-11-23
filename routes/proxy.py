# routes/proxy.py
from flask import Blueprint, request, jsonify
from models.log import log_request

bp = Blueprint("proxy", __name__, url_prefix="/api/proxy")

@bp.route("/", methods=["POST"])
def proxy_request():
    data = request.get_json(force=True)
    log_request({
        "action":"proxy_request",
        "url":data.get("url"),
        "method":data.get("method"),
        "ip": request.remote_addr
    })
    return jsonify({"status":"logged"}), 200

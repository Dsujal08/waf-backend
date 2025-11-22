from flask import Blueprint, request, jsonify
from utils.waf_engine import inspect_request

bp = Blueprint("proxy", __name__, url_prefix="/api/proxy")

@bp.route("/<path:rest>", methods=["GET","POST","PUT","DELETE"])
def proxy(rest):
    blocked, rule = inspect_request(request)
    if blocked:
        return jsonify({"error":"Blocked by WAF", "rule": rule}), 403
    return jsonify({"ok": True, "path": rest})

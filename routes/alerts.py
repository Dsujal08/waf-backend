# routes/alerts.py
from flask import Blueprint, request, jsonify
from config import ALERTS
from datetime import datetime
from models.log import log_request

bp = Blueprint("alerts", __name__, url_prefix="/api/alerts")

@bp.route("/", methods=["GET"])
def list_alerts():
    alerts = list(ALERTS.find().sort("timestamp",-1))
    for a in alerts:
        a["_id"] = str(a["_id"])
    return jsonify(alerts)

@bp.route("/", methods=["POST"])
def create_alert():
    body = request.get_json(force=True)
    body["timestamp"] = datetime.utcnow()
    res = ALERTS.insert_one(body)
    log_request({"action":"alert_created","alert_id":str(res.inserted_id),"ip":request.remote_addr})
    return jsonify({"id": str(res.inserted_id)}), 201

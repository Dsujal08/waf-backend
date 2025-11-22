# routes/alerts.py
from flask import Blueprint, request, jsonify
from services.alert_service import create_alert, list_alerts

bp = Blueprint("alerts", __name__, url_prefix="/api")

@bp.route("/alerts", methods=["POST"])
def api_create_alert():
    doc = request.get_json()
    if not doc:
        return jsonify({"error": "No data provided"}), 400
    create_alert(doc)
    return jsonify({"success": True}), 201

@bp.route("/alerts", methods=["GET"])
def api_list_alerts():
    alerts = list_alerts()
    return jsonify(alerts), 200

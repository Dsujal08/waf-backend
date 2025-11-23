# routes/rules.py
from flask import Blueprint, request, jsonify
from config import RULES
from bson import ObjectId
from models.log import log_request

bp = Blueprint("rules", __name__, url_prefix="/api/rules")

@bp.route("/", methods=["GET"])
def get_rules():
    rules = list(RULES.find())
    for r in rules:
        r["_id"] = str(r["_id"])
    return jsonify(rules)

@bp.route("/", methods=["POST"])
def add_rule():
    body = request.get_json(force=True)
    res = RULES.insert_one(body)
    log_request({"action":"rule_created","rule_id":str(res.inserted_id),"ip":request.remote_addr})
    return jsonify({"id": str(res.inserted_id)}), 201

@bp.route("/<rule_id>", methods=["PUT"])
def update_rule(rule_id):
    body = request.get_json(force=True)
    RULES.update_one({"_id": ObjectId(rule_id)}, {"$set": body})
    log_request({"action":"rule_updated","rule_id":rule_id,"ip":request.remote_addr})
    return jsonify({"status":"ok"}), 200

@bp.route("/<rule_id>", methods=["DELETE"])
def delete_rule(rule_id):
    RULES.delete_one({"_id": ObjectId(rule_id)})
    log_request({"action":"rule_deleted","rule_id":rule_id,"ip":request.remote_addr})
    return jsonify({"status":"deleted"}), 200

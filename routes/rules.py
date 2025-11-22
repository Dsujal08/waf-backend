from flask import Blueprint, request, jsonify
from models.rule import list_rules, create_rule, update_rule, delete_rule

bp = Blueprint("rules", __name__, url_prefix="/api/rules")

@bp.route("/", methods=["GET"])
def get_rules():
    return jsonify(list_rules())

@bp.route("/", methods=["POST"])
def post_rule():
    doc = request.get_json(force=True)
    rid = create_rule(doc)
    return jsonify({"id": rid}), 201

@bp.route("/<rid>", methods=["PATCH"])
def patch_rule(rid):
    patch = request.get_json(force=True)
    update_rule(rid, patch)
    return jsonify({"ok": True})

@bp.route("/<rid>", methods=["DELETE"])
def del_rule(rid):
    delete_rule(rid)
    return jsonify({"ok": True})

from flask import Blueprint, request, jsonify
from models.item_model import add_item, list_items, get_item, delete_item

bp = Blueprint("items", __name__, url_prefix="/api/items")

@bp.route("/", methods=["GET"])
def get_items():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 50))
    skip = page * size
    return jsonify({"ok": True, "data": list_items(skip=skip, limit=size)})

@bp.route("/", methods=["POST"])
def create_item():
    body = request.get_json(force=True)
    new_id = add_item(body)
    return jsonify({"ok": True, "id": new_id}), 201

@bp.route("/<id>", methods=["DELETE"])
def remove_item(id):
    delete_item(id)
    return jsonify({"ok": True})

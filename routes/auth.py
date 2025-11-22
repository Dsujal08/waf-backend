# routes/auth.py
from flask import Blueprint, request, jsonify
from models.user import create_user, find_by_email, get_public
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt  # fixed import

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# POST /api/auth/signup
@bp.route("/signup", methods=["POST"])
def signup():
    body = request.get_json(force=True)
    email = body.get("email")
    password = body.get("password")
    role = body.get("role", "viewer")
    name = body.get("name")

    # Validate inputs
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    if find_by_email(email):
        return jsonify({"error": "user exists"}), 400

    # create user
    uid = create_user(email, password, role, name)

    # generate JWT token
    token = create_access_token(identity={
        "email": email,
        "role": role,
        "id": uid
    })

    return jsonify({"token": token, "id": uid}), 201


# POST /api/auth/login
@bp.route("/login", methods=["POST"])
def login():
    body = request.get_json(force=True)
    email = body.get("email")
    password = body.get("password")

    user = find_by_email(email)
    if not user:
        return jsonify({"error": "invalid credentials"}), 401

    # verify password
    if not bcrypt.verify(password, user["password"]):
        return jsonify({"error": "invalid credentials"}), 401

    # create JWT token
    token = create_access_token(identity={
        "email": user["email"],
        "role": user.get("role", "viewer"),
        "id": str(user["_id"])
    })

    return jsonify({"token": token, "user": get_public(user)}), 200

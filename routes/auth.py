from flask import Blueprint, request, jsonify
from models.user import create_user, find_by_email, get_public
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt
from models.log import log_request
from datetime import datetime

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# --------------------------
# POST /signup
# --------------------------
@bp.route("/signup", methods=["POST"])
def signup():
    body = request.get_json(force=True)
    email = body.get("email")
    password = body.get("password")
    role = body.get("role", "viewer")
    name = body.get("name")

    if not email or not password:
        log_request({
            "action": "signup_failed",
            "email": email,
            "reason": "missing_email_or_password",
            "ip": request.remote_addr
        })
        return jsonify({"error": "Email and password are required"}), 400

    if find_by_email(email):
        log_request({
            "action": "signup_failed",
            "email": email,
            "reason": "user_exists",
            "ip": request.remote_addr
        })
        return jsonify({"error": "User already exists"}), 400

    uid = create_user(email, password, role, name)

    log_request({
        "action": "signup_success",
        "email": email,
        "user_id": str(uid),
        "ip": request.remote_addr
    })

    # JWT: identity is the user ID (string), role as additional_claims
    token = create_access_token(identity=str(uid), additional_claims={"role": role, "email": email})

    return jsonify({"token": token, "id": str(uid)}), 201


# --------------------------
# POST /login
# --------------------------
@bp.route("/login", methods=["POST"])
def login():
    body = request.get_json(force=True)
    email = body.get("email")
    password = body.get("password")

    user = find_by_email(email)
    if not user:
        log_request({
            "action": "login_failed",
            "email": email,
            "role": "user",  # default
            "reason": "user_not_found",
            "ip": request.remote_addr
        })
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.verify(password, user["password"]):
        log_request({
            "action": "login_failed",
            "email": email,
            "role": user.get("role", "user"),
            "reason": "wrong_password",
            "ip": request.remote_addr
        })
        return jsonify({"error": "Invalid credentials"}), 401

    # JWT: identity is user ID, extra info in additional_claims
    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": user.get("role", "user"), "email": user["email"]}
    )

    # ⭐ FIXED: Now log_request receives the REAL ROLE
    log_request({
        "action": "login_success",
        "email": user["email"],
        "role": user.get("role", "user"),   # <---- THIS FIXES YOUR ISSUE
        "user_id": str(user["_id"]),
        "ip": request.remote_addr
    })

    return jsonify({"token": token, "user": get_public(user)}), 200

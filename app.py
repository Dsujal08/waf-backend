import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# ======================
# Load Environment
# ======================
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret_here")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
PORT = int(os.getenv("FLASK_RUN_PORT", 5000))

# ======================
# Initialize Flask App
# ======================
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET

# Enable CORS
CORS(
    app,
    resources={r"/*": {"origins": FRONTEND_URL}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)


# JWT Manager
jwt = JWTManager(app)

# ======================
# Import Blueprints
# ======================
from routes.auth import bp as auth_bp
from routes.admin import bp as admin_bp
from routes.rules import bp as rules_bp
from routes.logs import bp as logs_bp    # FIXED NAME
from routes.alerts import bp as alerts_bp
from routes.proxy import bp as proxy_bp

# ======================
# Register Blueprints
# ======================
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(rules_bp)
app.register_blueprint(logs_bp)          # FIXED NAME
app.register_blueprint(alerts_bp)
app.register_blueprint(proxy_bp)

# ======================
# Health Check Endpoint
# ======================
@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"message": "ok"}), 200

# ======================
# Run App
# ======================
if __name__ == "__main__":
    print(f"🚀 Flask API running at http://0.0.0.0:{PORT}")
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True
    )

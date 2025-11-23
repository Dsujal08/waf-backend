# app.py
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sockets.socketio_app import socketio

# Import Blueprints
from routes.auth import bp as auth_bp
from routes.admin import bp as admin_bp
from routes.rules import bp as rules_bp
from routes.logs import bp as logs_bp
from routes.alerts import bp as alerts_bp
from routes.proxy import bp as proxy_bp

# Load environment variables
load_dotenv()

# -------------------------
# Flask app setup
# -------------------------
app = Flask(__name__)

# Allow requests from Next.js frontend
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# JWT setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "your_jwt_secret_here")
jwt = JWTManager(app)

# -------------------------
# Register Blueprints
# -------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(rules_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(proxy_bp)

# Test route
@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"message": "ok"}), 200

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    # Use threading for SocketIO to avoid eventlet issues on Windows
    socketio.init_app(
        app,
        cors_allowed_origins="http://localhost:3000",
        async_mode="threading"
    )
    print("🚀 Server running at http://0.0.0.0:5000")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

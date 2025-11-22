# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sockets.socketio_app import socketio
from routes.auth import bp as auth_bp
from routes.rules import bp as rules_bp
from routes.logs import bp as logs_bp
from routes.alerts import bp as alerts_bp
from routes.proxy import bp as proxy_bp
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://MernAuth:admin1@cluster0.xpgba.mongodb.net/wafdb")
JWT_SECRET = os.getenv("JWT_SECRET", "f2d9c4a1b3e9f6d7a8c9e0f1d2b3a4c5e6f7d8a9b0c1d2e3f4a5b6c7d8e9f0a1")  # default secret if missing
SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE", "")  # optional Redis

# MongoDB setup
client = MongoClient(MONGO_URI)
DB = client.get_database("wafdb")
USERS = DB["users"]
RULES = DB["waf_rules"]
LOGS = DB["logs"]
ALERTS = DB["alerts"]
ITEMS = DB["items"]

# Flask app setup
app = Flask(__name__)
CORS(app)

# JWT setup (must be before blueprints)
app.config["JWT_SECRET_KEY"] = JWT_SECRET
jwt = JWTManager(app)  # ✅ initialize JWTManager

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(rules_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(proxy_bp)

# Simple test route
@app.route("/api/ping")
def ping():
    return jsonify({"message": "ok"}), 200

# Run server
if __name__ == "__main__":
    # Initialize SocketIO with Flask app
    socketio.init_app(app, cors_allowed_origins="*")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)  # debug=True for full error messages

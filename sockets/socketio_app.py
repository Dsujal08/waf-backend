# sockets/socketio_app.py
from flask_socketio import SocketIO

# Initialize SocketIO without attaching to app yet
socketio = SocketIO(cors_allowed_origins="*")

# Example event handlers
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

@socketio.on("message")
def handle_message(msg):
    print("Message received:", msg)
    socketio.send(f"Server received: {msg}")

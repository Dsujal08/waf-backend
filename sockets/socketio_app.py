from flask_socketio import SocketIO
from config import SOCKETIO_MESSAGE_QUEUE

socketio = SocketIO(cors_allowed_origins="*", async_mode="threading",
                    message_queue=SOCKETIO_MESSAGE_QUEUE or None)

# 🔥 Fix: Add this function
def broadcast_alert(alert):
    """
    Emits alert to all connected clients on 'waf_alert' channel.
    """
    try:
        socketio.emit("waf_alert", alert, broadcast=True)
    except Exception as e:
        print("Socket emit error:", e)

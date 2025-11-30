# import asyncio
# import websockets
# import json
# from datetime import datetime

# ADMIN_CLIENTS = set()

# async def notify_admins(event_data):
#     """Send a message to all connected admin clients"""
#     if ADMIN_CLIENTS:
#         message = json.dumps(event_data)
#         await asyncio.wait([client.send(message) for client in ADMIN_CLIENTS])

# async def handler(ws):
#     print("Client connected")

#     try:
#         # First message identifies client type
#         init = await ws.recv()
#         data = json.loads(init)

#         if data.get("type") == "admin":
#             ADMIN_CLIENTS.add(ws)
#             print("Admin connected")
#         else:
#             print("Normal user connected")

#             # Example: send a login notification to all admins
#             event = {
#                 "type": "login_notification",
#                 "time": datetime.utcnow().isoformat(),
#                 "email": data.get("email", "unknown@example.com"),
#                 "ip": data.get("ip", "127.0.0.1"),
#                 "device": data.get("device", "Unknown Device"),
#             }
#             await notify_admins(event)

#         # Keep listening to client messages
#         async for msg in ws:
#             print("Received:", msg)

#     except Exception as e:
#         print("Client disconnected:", e)
#     finally:
#         if ws in ADMIN_CLIENTS:
#             ADMIN_CLIENTS.remove(ws)

# async def main():
#     print("WebSocket running on ws://localhost:5001")
#     async with websockets.serve(handler, "0.0.0.0", 5001):
#         await asyncio.Future()  # keep running

# asyncio.run(main())
import asyncio
import websockets
import json
from datetime import datetime

ADMIN_CLIENTS = set()

async def notify_admins(event_data):
    if ADMIN_CLIENTS:
        message = json.dumps(event_data)
        # Create tasks for sending to prevent blocking if one client is slow
        await asyncio.gather(*[client.send(message) for client in ADMIN_CLIENTS], return_exceptions=True)

async def handler(ws):
    print(f"Client attempting connection from {ws.remote_address}")

    try:
        # Wait for the identification message
        init = await ws.recv()
        data = json.loads(init)

        if data.get("type") == "admin":
            ADMIN_CLIENTS.add(ws)
            print("✅ Admin connected")
        else:
            print("👤 Normal user connected")
            # Logic to trigger notification...
            event = {
                "type": "login_notification",
                "time": datetime.utcnow().isoformat(),
                "email": data.get("email", "unknown@example.com"),
                "ip": data.get("ip", "127.0.0.1"),
                "device": data.get("device", "Unknown Device"),
            }
            await notify_admins(event)

        # Keep connection open
        async for msg in ws:
            pass # Just listen to keep the connection alive

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ws in ADMIN_CLIENTS:
            ADMIN_CLIENTS.remove(ws)
            print("❌ Admin removed")

async def main():
    print("WebSocket running on ws://localhost:5001")
    # 👇 FIX: Add origins=None to allow connections from Next.js (port 3000)
    async with websockets.serve(handler, "0.0.0.0", 5001, origins=None): 
        await asyncio.Future()  # keep running

if __name__ == "__main__":
    asyncio.run(main())
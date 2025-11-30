import asyncio
import websockets
import json

ADMIN_CLIENTS = set()

async def handler(ws, path):
    print("Client connected")

    try:
        # First message must identify client type
        init = await ws.recv()
        data = json.loads(init)

        if data.get("type") == "admin":
            ADMIN_CLIENTS.add(ws)
            print("Admin connected")
        else:
            print("Normal user connected")

        # Listen for messages
        async for msg in ws:
            print("Received:", msg)

    except:
        print("Client disconnected")
    finally:
        if ws in ADMIN_CLIENTS:
            ADMIN_CLIENTS.remove(ws)

async def main():
    print("WebSocket running on ws://localhost:5001")
    async with websockets.serve(handler, "0.0.0.0", 5001):
        await asyncio.Future()

asyncio.run(main())

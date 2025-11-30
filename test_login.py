import asyncio
import websockets
import json
import random

async def simulate_user():
    uri = "ws://127.0.0.1:5001"
    
    try:
        async with websockets.connect(uri) as websocket:
            # Fake User Data
            user_data = {
                "type": "user",
                "email": f"new_user_{random.randint(1000,9999)}@gmail.com",
                "ip": f"192.168.1.{random.randint(10,99)}",
                "device": "Chrome / Windows 11"
            }
            
            print(f"📤 Sending login: {user_data['email']}")
            await websocket.send(json.dumps(user_data))
            print("✅ Sent successfully!")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_user())
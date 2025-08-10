# websocket_server.py

import asyncio
import websockets

async def handler(websocket):
    print("✅ Client connected!")
    try:
        async for message in websocket:
            print(f"📥 Message from Unity: {message}")
            await websocket.send("Hello from Python WebSocket Server!")
    except websockets.ConnectionClosed:
        print("❌ Connection closed")

async def main():
    print("🚀 Python WebSocket server starting on ws://localhost:6790")
    async with websockets.serve(handler, "localhost", 6790):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

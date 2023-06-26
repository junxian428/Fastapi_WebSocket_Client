import asyncio
from fastapi import FastAPI
import websockets
import json

app = FastAPI()

websocket_connection = None

async def establish_websocket_connection():
    global websocket_connection
    websocket_connection = await websockets.connect("ws://localhost:8088/user")

asyncio.create_task(establish_websocket_connection())

@app.post("/send")
async def send_to_websocket(payload: dict):
    if websocket_connection is not None:
        message = json.dumps(payload)
        await websocket_connection.send(message)
        print(message)
        response = await websocket_connection.recv()
        return {"response": response}
    else:
        return {"error": "WebSocket connection is not available"}


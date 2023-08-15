import asyncio
import websockets

async def echo(websocket, path):
  async for message in websocket:
    print(f"Received message: {message}")
    await websocket.send(f"{message}")

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
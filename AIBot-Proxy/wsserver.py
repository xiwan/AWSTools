import asyncio
import websockets

async def echo(websocket, path):
  async for message in websocket:
    print(f"Received message: {message}")
    await websocket.send(f"{message}")
    print(f"Send message: {message}")
    # await websocket.send(f"{message}")
    # print(f"Send message: {message}")

async def testSend(websocket, path):
  message = "test"
  print(f"Send message: {message}")
  await websocket.send(f"{message}")
  print(f"Send message: {message}")
  await websocket.send(f"{message}")
  await echo(websocket, path)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
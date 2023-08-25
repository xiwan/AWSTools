import asyncio
import websockets
import json

async def echo(websocket, path):
  async for message in websocket:
    print(f"Received message: {message}")
    await websocket.send(f"{message}")
    print(f"Send message: {message}")
    # await websocket.send(f"{message}")
    # print(f"Send message: {message}")

async def testSend(websocket, path):
  message = "test"
  await websocket.send(f"{message}")
  print(f"Send message text: {message}")

  message2 = Getbyte(1017) + GetPayload(1017)
  await websocket.send(message2)
  print(f"Send message binary: {message2}")

  message3 = Getbyte(4096) + GetPayload(4096)
  await websocket.send(message3)
  print(f"Send message binary: {message3}")

  message4 = Getbyte(4993) + GetPayload(4993)
  await websocket.send(message4)
  print(f"Send message binary: {message4}")

  message5 = Getbyte(4993) + GetPayload(4993)
  await websocket.send(message5)
  print(f"Send message binary: {message5}")

  await echo(websocket, path)

def Getbyte(CSID): 
  return CSID.to_bytes(4, byteorder='little')

def GetPayload(code):
  J = {
      "script_id": code
  }
  J = json.dumps(J)
  J = J.encode()
  return J

start_server = websockets.serve(testSend, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
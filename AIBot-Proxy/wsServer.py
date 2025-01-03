import asyncio
import websockets
import json
import argparse

async def echo(websocket, path):
  async for message in websocket:
    print(f"Received message: {message}")
    await websocket.send(f"{message}")
    print(f"Send message: {message}")
    # await websocket.send(f"{message}")
    # print(f"Send message: {message}")
    pass

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
  pass

def Getbyte(CSID): 
  return CSID.to_bytes(4, byteorder='little')

def GetPayload(code):
  J = {
      "script_id": code
  }
  J = json.dumps(J)
  J = J.encode()
  return J

if __name__ == '__main__':  
  parser = argparse.ArgumentParser(description='tcp server command-line options')
  parser.add_argument('--host', type=str, help='host address: 0.0.0.0 or localhost', default='localhost')
  parser.add_argument('--port', type=int, help='host port number: 8765', default='8765')
  args = parser.parse_args()

  start_server = websockets.serve(echo, args.host, args.port)

  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()
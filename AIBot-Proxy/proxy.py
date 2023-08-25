
import time
import threading
import websockets

from wsHandler import CustomThread
from httpServer import manager, run_async, remoteUri, logging
from wssClient import WssConnector

# wsClient = None

# @run_async
# async def OnConnect(connectUri):
#     async with websockets.connect(connectUri) as websocket:
#         print(f"In [wsclient] flask global level: {threading.current_thread().name}")
#         wsClient = websocket
#         message = "Hello, server!"
#         await wsClient.send(message)
#         logging.info(f"Sent: {message}")

#         response = await wsClient.recv()
#         logging.info(f"Received: {response}")

if __name__ == "__main__":
    s = time.time()
    print(f"In [{threading.current_thread().name}] flask global id: {str(threading.current_thread().ident)}")

    wss = WssConnector()
    
    httpRev1 = CustomThread(manager.run, ())
    wsAdaptor = CustomThread(wss.OnConnect, (remoteUri,))

    wsAdaptor.start()
    httpRev1.start()
    wsAdaptor.join()
    httpRev1.join()
    logging.info("Exit Main Program")



 




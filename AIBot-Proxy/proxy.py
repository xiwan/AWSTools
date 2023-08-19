
import time
import threading
import websockets
import logging

from wsHandler import CustomThread
from httpServer import manager, run_async, remoteUri, secretKey
from wssClient import WssConnector

logging.basicConfig(filename="test.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)

wsClient = None

@run_async
async def OnConnect(connectUri):
    async with websockets.connect(connectUri) as websocket:
        print(f"In [wsclient] flask global level: {threading.current_thread().name}")
        wsClient = websocket
        message = "Hello, server!"
        await wsClient.send(message)
        logging.info(f"Sent: {message}")

        response = await wsClient.recv()
        logging.info(f"Received: {response}")

if __name__ == "__main__":
    s = time.time()
    logging.info(f"In [Main] flask global level: {threading.current_thread().name}")

    wss = WssConnector()
    
    httpRev1 = CustomThread(manager.run, ())
    wsAdaptor = CustomThread(wss.OnConnect, (remoteUri,))

    wsAdaptor.start()
    httpRev1.start()
    wsAdaptor.join()
    httpRev1.join()
    logging.info("Exit Main Program")



 




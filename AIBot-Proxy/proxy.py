
import time
import threading
import websockets

from wsHandler import CustomThread
from httpServer import manager, run_async, remoteUri, logging
from wssClient import WssConnector

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



 




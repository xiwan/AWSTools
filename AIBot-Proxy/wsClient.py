
import threading
import websockets
import logging
import json
import queue
import _thread as thread

from Core.runAsync import run_async, remoteUri, secretKey

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class ConnectorPool(object):
    def __init__(self):
        pass
        self.pool = {}

    def RegConn(self, key, conn):
        self.pool[key] = conn
        # print(key, len(self.pool.keys()))

    def GetConn(self, key):
        if key in self.pool.keys():
            return self.pool.get(key)
        else:
            return None
        
    def BuildConns(self, remoteUri):
        while True:
            for key in self.pool.keys():
                self.GetConn(key).OnConnect(remoteUri)
                

class ConnectorKls(object):
    def __init__(self):
        pass
        self.ws = None
        self.inQ = queue.Queue()
        self.outQ = queue.Queue()
          
    def GetConnector(self):
        if self.ws == None:
            self.OnConnect(self.remoteUri)
        return self.ws
    
    def PutInMsg(self, msg):
        print(msg)
        self.inQ.put(msg)
    
    def PutOutMsg(self, msg):
        self.outQ.put(msg)

    async def DeliverMsg(self):
        while True:
            msg = self.inQ.get()
            print(f'In Working on {msg}')

            await self.async_sendJsonObj(msg)
            print(f"In Sent: {msg}")

            res = await self.ws.recv()
            print(f"In Received: {res}")
            self.PutOutMsg(res)
            self.inQ.task_done()

    async def ReceiveMsg(self):     
        while True:
            res = await self.ws.recv()
            print(f"Out Received: {res}")
            self.PutOutMsg(res)
            self.outQ.task_done()  

    async def FetchMsg(self):
        while True:
            msg = self.outQ.get()
            print(f'Out Working on {msg}')
            self.outQ.task_done()
            return msg
    
    async def async_sendJsonObj(self, cmd):
        return await self.ws.send(json.dumps(cmd))
    
    async def async_sendByte(self, cmd):
        return await self.ws.send(cmd)
    
    async def async_close(self):
        await self.ws.close(reason="user quit")
        self.ws = None

    @run_async
    async def OnConnect(self, remoteUri):
        self.remoteUri = remoteUri
        async with websockets.connect(self.remoteUri) as websocket:
            print(f"In [wsclient] flask global level: {threading.current_thread().name}")
            self.ws = websocket

            # thread.start_new_thread(self.ReceiveMsg, ())
            # thread.start_new_thread(self.DeliverMsg, ())
            await self.ReceiveMsg()
            await self.DeliverMsg()
            

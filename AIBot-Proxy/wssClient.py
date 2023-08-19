import websocket
import _thread as thread
import time
import json
import queue

from Core.runAsync import run_async, remoteUri, secretKey, binary

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class WssConnector(object):
    def __init__(self):
        pass
        self.ws = None
        self.remoteUri = None
        self.inQ = queue.Queue() # request message queue
        self.outQ = queue.Queue() # response message queue
        self.stateQ = queue.Queue() # state messsage queue

    def GetConnector(self):
        if self.ws == None:
            self.OnConnect(self.remoteUri)
        return self.ws
    
    def PutInMsg(self, msg):
        self.inQ.put(msg)
    
    def PutOutMsg(self, msg):
        self.outQ.put(msg)

    def SendJson(self, cmd):
        return self.ws.send(json.dumps(cmd))
    
    def SendByte(self, cmd):
        return self.ws.send(cmd)
    
    async def async_close(self):
        await self.ws.close(reason="user quit")
        self.ws = None

    def Run(self, *args):
        while True:
            msg = self.inQ.get()
            print(f"In Sent {binary} format: {msg}")
            if binary == 1:
                self.SendByte(msg) # .encode('utf-8') for binary
            else:
                self.SendJson(msg)
            
            self.inQ.task_done()

    async def FetchMsg(self):
        while True:
            msg = self.outQ.get()
            print(f'### FetchMsg ### {msg}')
            self.outQ.task_done()
            return msg

    def OnMessage(self, ws, msg):
        print(f"### OnMessage ###: {msg}")
        self.PutOutMsg(msg)

    def OnError(self, ws, error):
        print(error)

    def OnClose(self, ws, close_status_code, close_msg):
        print(f"### closed ### {close_status_code} : {close_msg}")
        self.ws = None
        self.remoteUri = None

    def OnOpen(self, ws):
        print("### Opened connection ###")
        thread.start_new_thread(self.Run, ())

    @run_async
    async def OnConnect(self, remoteUri):
        websocket.enableTrace(False)
        self.remoteUri = remoteUri
        self.ws = websocket.WebSocketApp(
            self.remoteUri,
            on_open=self.OnOpen,
            on_message=self.OnMessage,
            on_error=self.OnError,
            on_close=self.OnClose)
        
        self.ws.run_forever(reconnect=5)
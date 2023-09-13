import websocket
import _thread as thread
import time
import json
import queue
import asyncio

from Core.utils import run_async, decodeLittle, decodeBig, getbyteLitte, singleton, logging, config, routeTable

remoteUri = config['remoteUri']
secretKey = config['secretKey']
wssdata = int(config['wssdata'])

@singleton
class WssConnector(object):
    def __init__(self):
        pass
        self.ws = None
        self.remoteUri = None
        self.lastState = None
        self.inQ = queue.Queue() # request message queue
        self.outQ = queue.Queue() # response message queue
        self.stateQ = queue.Queue() # state messsage queue

        self.stateDict = {}
        for code in eval(routeTable['state']):
            self.stateDict[code] = queue.Queue()
        logging.info(f"### WssConnector create stateDict ### size: {len(self.stateDict)} ")


    def GetConnector(self):
        if self.ws == None:
            self.OnConnect(self.remoteUri)
        return self.ws
    
    def PutInMsg(self, msg):
        self.inQ.put(msg)
    
    def PutOutMsg(self, msg):
        self.outQ.put(msg)
    
    def PutSateMsg(self, msg):
        self.stateQ.put(msg)

    def PutSateDictMsg(self, code, msg):
        if code in self.stateDict:
            self.stateDict[code].put(msg)

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
            logging.info(f"### Run ### {wssdata} format: {msg}")
            if wssdata == 1:
                self.SendByte(msg) 
            else:
                self.SendJson(msg)
            
            self.inQ.task_done()

    async def FetchMsg(self):
        while True:
            await asyncio.sleep(0.1)
            try:
                msg = self.outQ.get(timeout=0.5)
                self.outQ.task_done()
            except queue.Empty: 
                logging.info(f"Out queue.Empty")
                msg = getbyteLitte(0000)    
            logging.info(f'### FetchMsg ### {msg}')
            return msg
        
    async def FetchSateMsg(self):
        while True:
            await asyncio.sleep(0.1)
            try:
                msg = self.stateQ.get(timeout=0.3)
                if not msg is None:
                    self.lastState = msg
                self.stateQ.task_done()
            except Exception as error: 
                logging.info(f"State queue.Empty")
                if not self.lastState is None:
                    msg = self.lastState
                else:
                    msg = getbyteLitte(0000)
            logging.info(f'### FetchSateMsg ### {msg} ')

            return msg
        
    async def FetchSateDictMsg(self, code):
        while True:
            await asyncio.sleep(0.1)
            try:
                msg = None
                if code in self.stateDict:
                    msg = self.stateDict[code].get(timeout=0.3)
                
                # return all state
                if not msg is None:
                    self.lastState = msg
                    
                self.stateDict[code].task_done()
            except Exception as error: 
                logging.info(f"{code} queue.Empty")
                if not self.lastState is None:
                    msg = self.lastState
                else:
                    msg = getbyteLitte(0000)
            logging.info(f'### FetchSateDictMsg ### {code}={msg} ')

            return msg

    def OnMessage(self, ws, msg):
        if isinstance(msg, bytes):
            code = decodeLittle(msg[:4])
            if code in eval(routeTable['state']):
                # self.PutSateMsg(msg)
                self.PutSateDictMsg(code, msg)
            else :
                self.PutOutMsg(msg)

            logging.info(f"### OnMessage bytes ###: {msg}")

        elif isinstance(msg, str):
            self.PutOutMsg(msg)
            logging.info(f"### OnMessage str ###: {msg}")
            

    def OnError(self, ws, error):
        logging.info(error)

    def OnClose(self, ws, close_status_code, close_msg):
        logging.info(f"### closed ### {close_status_code} : {close_msg}")
        self.ws = None
        self.remoteUri = None
        self.lastState = None

    def OnOpen(self, ws):
        logging.info("### Opened connection ###")
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
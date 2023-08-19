import json
import logging
import threading
from websockets import connect

class Handler:
    def __init__(self, loop=None):
        self.ws = None
        self.loop = loop

    async def async_connect(self, url):
        print(f"In [Handler] flask global level: {threading.current_thread().name}")
        logging.info("attempting connection to {}".format(url))
        # perform async connect, and store the connected WebSocketClientProtocol
        # object, for later reuse for send & recv
        self.ws = await connect(url)
        logging.info("connected")

    def sendJsonObj(self, cmd):
        return self.loop.run_until_complete(self.async_sendJsonObj(cmd))

    async def async_sendJsonObj(self, cmd):
        return await self.ws.send(json.dumps(cmd))

    def sendByte(self, cmd):
        return self.loop.run_until_complete(self.async_sendByte(cmd))

    async def async_sendByte(self, cmd):
        return await self.ws.send(cmd)

    def close(self):
        self.loop.run_until_complete(self.async_close())
        logging.info('closed')

    async def async_close(self):
        await self.ws.close(reason="user quit")
        self.ws = None

    def toRecv(self):
        self.loop.run_until_complete(self.async_recv())

    async def async_recv(self, callback=None):
        # i = 1
        logging.info('async_recv begin')
        while True:
            # logging.info('to recv:')
            reply = await self.ws.recv()
            if callback:
                callback(reply)
            # logging.info("{}- recv: {}".format(i, reply))
            # i += 1

        logging.info('async_recv end')


# 创建 Thread 的子类
class CustomThread(threading.Thread):
    def __init__(self, func, args):
        '''
        :param func: 可调用的对象
        :param args: 可调用对象的参数
        '''
        threading.Thread.__init__(self, target=func, args=args)
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        # print(self.func)
        # print(*self.args)
        self.result = self.func(*self.args)
        print(self.result)

    def getResult(self):
        return self.result
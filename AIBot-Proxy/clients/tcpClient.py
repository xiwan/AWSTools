import socket
import _thread as thread
import time
import json
import queue
import asyncio

from Core.utils import run_async, decodeLittle, decodeBig, getbyteLitte, singleton, logging, config, routeTable

remoteTcp = config['remoteTcp']
secretKey = config['secretKey']
binary = config['binary']

@singleton
class TcpConnector(object):
    def __init__(self):
        self.tcp_socket = None
        self.server_addr = None
        self.remoteTcp = None
        self.lastState = None
        self.inQ = queue.Queue() # request message queue
        self.outQ = queue.Queue() # response message queue
        self.stateQ = queue.Queue() # state messsage queue

        self.stateDict = {}
        for code in eval(routeTable['state']):
            self.stateDict[code] = queue.Queue()
        logging.info(f"### TcpConnector create stateDict ### size: {len(self.stateDict)} ")

    def GetConnector(self):
        if self.tcp_socket == None:
            self.OnConnect(self.remoteUri)
        return self.tcp_socket

    def PutInMsg(self, msg):
        self.inQ.put(msg)
    
    def PutOutMsg(self, msg):
        self.outQ.put(msg)
    
    def PutSateMsg(self, msg):
        self.stateQ.put(msg)

    def PutSateDictMsg(self, code, msg):
        if code in self.stateDict:
            self.stateDict[code].put(msg)

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

    def OnOpen(self):
        while True:
            msg = self.inQ.get()
            logging.info(f"### Run ### {binary} format: {msg}")
            self.SendByte(str(msg).encode("utf-8"))
            self.inQ.task_done()

    def OnMessage(self):
        revcdata = self.tcp_socket.recv(1024)
        if isinstance(revcdata, bytes):
            msg = revcdata.decode(encoding='utf-8')
            self.PutOutMsg(msg)
            logging.info(f"### OnMessage bytes ###: {msg}")
        elif isinstance(msg, str):
            self.PutOutMsg(msg)
            logging.info(f"### OnMessage str ###: {msg}")

    def Connect(self, server_addr, on_open=None, on_message=None, on_error=None, on_close=None):
        failed_try = 0
        while True:
            try:
                logging.info(f"start connect to server: {server_addr}")
                server_addr_array = server_addr.split(":")
                self.server_addr = (server_addr_array[0], int(server_addr_array[1]))
                self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_socket.connect(self.server_addr)
                break
            except socket.error as e:
                logging.info(f"### WssConnector Connect ### socket.error: {e}")
                failed_try += 1
                if failed_try > 3:
                    return
                time.sleep(1)

        #get the socket send buffer size and receive buffer size
        s_send_buffer_size = self.tcp_socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        s_receive_buffer_size = self.tcp_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        print("client TCP send buffer size is %d" % s_send_buffer_size)
        print("client TCP receive buffer size is %d" %s_receive_buffer_size)

        if on_open is not None:
            on_open()
        
        if on_message is not None:
            on_message()


    def SendByte(self, send_data):
        print(f"send_data: {send_data}, {len(send_data)}")
        sendlen = 0
        while sendlen < len(send_data):
            successlen = self.tcp_socket.send(send_data[sendlen:])
            sendlen += successlen

    def Close(self):
        self.tcp_socket.close()

    @run_async
    async def OnConnect(self, remoteTcp):
        self.remoteTcp = remoteTcp
        self.Connect(remoteTcp, self.OnOpen, self.OnMessage)
        logging.info(f"### WssConnector OnConnect ### remoteUri: {remoteTcp}")
        pass

    


# # 1.创建socket
# tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # 2. 链接服务器
# server_addr = ("34.229.191.120", 7788)
# tcp_socket.connect(server_addr)

# # 3. 发送数据
# send_data = input("请输入要发送的数据：")
# tcp_socket.send(send_data.encode("gbk"))

# # 4. 关闭套接字
# tcp_socket.close()
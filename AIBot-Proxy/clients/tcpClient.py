import socket
import _thread as thread
import time
import json
import queue
import asyncio
import progen.python.omni.base_pb2 as base_pb2
import progen.python.omni.msg_pb2 as msg_pb2

from Core.utils import run_async, decodeLittle, decodeBig, getbyteLitte, singleton, logging, config, routeTable
from Core.protoKlass import ProtoKlass


remoteTcp = config['remoteTcp']
remoteHttp = config['remoteHttp']
secretKey = config['secretKey']
tcpdata = int(config['tcpdata'])

@singleton
class TcpConnector(object):
    def __init__(self):
        self.tcp_socket = None
        self.server_addr = None
        self.remoteTcp = None
        self.lastState = None
        self.revcdata = b''
        self.remainder = b''
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
        if not code in self.stateDict:
            self.stateDict[code] = queue.Queue()
        self.stateDict[code].put(msg)
        
    async def FetchMsg(self):
        while True:
            await asyncio.sleep(0.1)
            try:
                msg = self.outQ.get(timeout=0.5)
                self.outQ.task_done()
            except queue.Empty: 
                print(f"Out queue.Empty")
                msg = getbyteLitte(0000)    
            print(f'### FetchMsg ### {msg}')
            return msg
        
    async def FetchStateDictMsg(self, code):
        while True:
            await asyncio.sleep(0.1)
            try:
                msg = self.stateDict[code].get(timeout=0.5)
                self.stateDict[code].task_done()
            except queue.Empty:
                print(f"stateDict queue.Empty")
                msg = getbyteLitte(0000)
            print(f'### FetchSateDictMsg ### {msg}')
            return msg

    def OnOpen(self):
        failed_try = 0
        while True:
            try:
                msg = self.inQ.get()
                logging.info(f"### OnOpen {tcpdata} format: {msg}")
                if tcpdata == 1:
                    proto = ProtoKlass()
                    send_data = proto.sendPayload(msg)
                    #send_data = proto.SendHandler(str(msg))
                    self.SendByte(send_data)
                else:
                    self.SendByte(str(msg).encode('utf-8'))

                self.inQ.task_done()
            except Exception as e:
                logging.info(f"### TcpConnector OnOpen ### socket.error: {e}")
                failed_try += 1
                if failed_try > 3:
                    return
                time.sleep(1)

    def OnMessage(self):
        HEADER_SIZE = 4
        failed_try = 0
        while True:
            try:
                header = b""
                while len(header) < HEADER_SIZE:
                    chunk = self.tcp_socket.recv(HEADER_SIZE)
                    if not chunk:
                        self.Close()
                        return
                    header += chunk
                payload_length = decodeLittle(header)
                
                payload = b""
                while len(payload) < payload_length:
                    chunk = self.tcp_socket.recv(payload_length - len(payload))
                    if not chunk:
                        self.Close()
                        return
                    payload += chunk

                proto = ProtoKlass()
                protoData = proto.revPayloadProto(payload)
                if protoData == None:
                    break

                code = protoData.protoId
                protoName = msg_pb2.BattleProtoIds.Name(code)
                if protoName.lower().endswith('notify'):
                    self.PutSateDictMsg(code, protoData)
                else:
                    self.PutOutMsg(protoData)

                # print("revPayloadProto", protoData)
                logging.info(f"### OnMessage bytes ###: {protoData}")
                pass

                # self.revcdata += self.tcp_socket.recv(1024)
                # print("------------------")
                # print(self.revcdata)
                # print("------------------")
                # if len(self.revcdata) == 0:
                #     break
                #     # self.Close()
                #     # return
                # if isinstance(self.revcdata, bytes):
                #     # msg = revcdata.decode(encoding='utf-8')
                #     if tcpdata == 1:
                #         proto = ProtoKlass()
                #         protoData, self.remainder = proto.revPayloadProto(self.revcdata)
                #         if protoData == None:
                #             break;
                #         code = protoData.protoId
                #         protoName = msg_pb2.BattleProtoIds.Name(code)
                #         # protoData = proto.RevHandler(revcdata)
                #         if protoName.lower().endswith('notify'):
                #             self.PutSateDictMsg(code, protoData)
                #         else:
                #             self.PutOutMsg(protoData)
                #         self.revcdata = self.remainder
                #         print(len(self.revcdata))
                #         logging.info(f"### OnMessage bytes ###: {protoData}")
                #     else:
                #         self.PutOutMsg(self.revcdata.decode("utf-8"))
                # elif isinstance(self.revcdata, str):
                #     self.PutOutMsg(self.revcdata)
                #     logging.info(f"### OnMessage str ###: {self.revcdata}")
            except Exception as e:
                logging.info(f"### TcpConnector OnMessage ### socket.error: {e}")
                failed_try += 1
                if failed_try > 3:
                    return
                time.sleep(1)

    def Connect(self, server_addr, on_open=None, on_message=None, on_error=None, on_close=None):
        failed_try = 0
        while True:
            try:
                print(f"start connect to server: {server_addr}")
                server_addr_array = server_addr.split(":")
                self.server_addr = (server_addr_array[0], int(server_addr_array[1]))
                self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_socket.connect(self.server_addr)
                break
            except Exception as e:
                logging.info(f"### TcpConnector Connect ### socket.error: {e}")
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
            thread.start_new_thread(on_open, ())

        if on_message is not None:
            thread.start_new_thread(on_message, ())


    def SendByte(self, send_data):
        # print(f"send_data: {send_data}, {len(send_data)}")
        sendlen = 0
        while sendlen < len(send_data):
            successlen = self.tcp_socket.send(send_data[sendlen:])
            sendlen += successlen

    def Close(self):
        self.tcp_socket.close()

    @run_async
    async def OnConnect(self, remoteTcp):
        self.remoteTcp = remoteTcp
        self.Connect(remoteTcp, on_open = self.OnOpen, on_message = self.OnMessage)
        logging.info(f"### WssConnector OnConnect ### remoteUri: {remoteTcp}")
        pass


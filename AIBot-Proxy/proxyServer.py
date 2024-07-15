import uuid
import json

from flask import Flask, request, session, jsonify, has_request_context, copy_current_request_context
from flask_script import Manager
from functools import wraps
from Core.utils import remoteUri, remoteTcp, remoteTcp, secretKey, logging
from Core.utils import run_async, autoIdIncrementor, protoMsgConverter
from Core.utils import encodeLittle, encodeBig, decodeLittle, decodeBig
from Core.protoKlass import ProtoKlass
from clients.wssClient import WssConnector
from clients.tcpClient import TcpConnector

app = Flask(__name__)
app.secret_key = secretKey
manager = Manager(app)

mode = None
uid = None
ws = None # websocket connector
ts = None # tcp socket connector

clientIdGen = autoIdIncrementor()
serverIdGen = autoIdIncrementor()

@app.before_request
def before_reql(*args, **kwargs):

    global uid, ws, ts, mode
    uid = session.get("sessionid")
    if not uid:
        uid = uuid.uuid1()
        session["sessionid"] = uid

    mode = app.config['SERVER_MODE']
    if mode is not None:
        if mode == "wss" or  mode == "ws":
            ws = WssConnector()
            if not ws or not uid:
                return str(404)
            
        if mode == "tcp":
            ts = TcpConnector()
            if not ts or not uid:
                return str(404)
    else:
        return str(404)

    # finalize the global vars
    uid = session.get("sessionid")
    uid = remoteUri

    # print('------')
    # print(request.headers.get('Host'))
    # print(request.headers.get('Authorization'))
    # print(request.headers.get('Content-Type'))
    # print(request.headers.get('Accept'))
    pass

async def mainHandler(reqjson):
    # print(reqjson)
    if ws is not None:
        ws.PutInMsg(reqjson)
        return await ws.FetchMsg()
    if ts is not None:
        ts.PutInMsg(reqjson)
        return await ts.FetchMsg()
    
    return None

@app.route('/', methods=['GET', 'POST'])
@run_async
async def hello():
    return await mainHandler(request.get_json())

@app.route('/init', methods=['GET', 'POST'])
@run_async
async def init():
    return await mainHandler(request.get_json())

@app.route('/reset', methods=['GET', 'POST'])
@run_async
async def reset():
    return await mainHandler(request.get_json())

@app.route('/action', methods=['GET', 'POST'])
@run_async
async def action():
    return await mainHandler(request.get_json())

@app.route('/state', methods=['GET', 'POST'])
@run_async
async def state():
    if ws is None:
        return None
    
    reqjson = request.get_json() 
    # ws.PutInMsg(reqjson)
    code = 0
    if 'code' in reqjson:
        code = reqjson['code']

    return await ws.FetchSateDictMsg(code)

## proto
import progen.python.todolist_pb2 as TodoList
import progen.python.omni.base_pb2 as base_pb2
import progen.python.omni.msg_pb2 as msg_pb2

@app.route('/protos', methods=['GET', 'POST'])
@run_async
async def protos():
    my_list = TodoList.TodoList()
    my_list.owner_id = 77777
    my_list.owner_name = "Benxiwan"

    first_item = my_list.todos.add()
    first_item.state = TodoList.TaskState.Value("TASK_DONE")
    first_item.task = "Test ProtoBuf for Python"
    first_item.due_date = "31.10.2019"

    proto = ProtoKlass()

    bin = proto.SerializeToString(my_list)
    print(bin)

    print("==========")
    my_list2 = TodoList.TodoList()
    proto.ParseFromString(my_list2, bin)
    print(my_list2)
    return proto.MessageToJson(my_list)

@app.route('/omni', methods=['POST'])
@run_async
async def omni():
    proto = ProtoKlass()
    data = request.get_json()
    try:
        protoId = data.get('protoId')
        protoMsgReq, protoMsgRsp = protoMsgConverter(protoId)
        protoData = data.get('data', None)
        requestId = next(clientIdGen)
        print(f'==== {requestId}, {protoId}, {protoMsgReq}, {protoMsgRsp}, {protoData}===')

        if not hasattr(msg_pb2.BattleProtoIds, protoId):
            raise Exception(f"protoId {protoId} not found")
        
        if not hasattr(msg_pb2, protoMsgReq):
            raise Exception(f"protoMsgReq {protoMsgReq} not found")
        
        if not hasattr(msg_pb2, protoMsgRsp):
            raise Exception(f"protoMsgRsp {protoMsgRsp} not found")

        reqValue = getattr(msg_pb2, protoMsgReq)
        reqInstance = reqValue()
        if protoData is not None:
            proto.ParseDict(protoData, reqInstance)

        baseReq = base_pb2.BaseReq()
        baseReq.protoId = msg_pb2.BattleProtoIds.Value(protoId)
        baseReq.requestId = requestId
        if reqInstance is not None:
            baseReq.data = proto.SerializeToString(reqInstance)
        print(baseReq)
        # payload sent to server
        # client_payload = proto.sendPayload(baseReq)

        # server_payload = mockServer(client_payload)
        # return proto.revPayload(server_payload)
        protoPackage = await mainHandler(baseReq)
        jsonPackage = proto.MessageToJson(protoPackage)

        rspValue = getattr(msg_pb2, protoMsgRsp)
        rspInstance = rspValue()
        protoData = None
        if protoPackage.data is not None:
            proto.ParseFromString(rspInstance, protoPackage.data)
            jsonPackage["data"] = proto.MessageToJson(rspInstance)
            pass
        
        return jsonPackage
    except Exception as e:
        return {"Error": str(e)}

@app.route('/omni_test', methods=['POST'])
@run_async
async def omni_test():
    proto = ProtoKlass()
    data = request.get_json()
    try:
        protoId = data.get('protoId')
        protoMsgReq, protoMsgRsp = protoMsgConverter(protoId)
        protoData = data.get('data', None)
        requestId = next(clientIdGen)
        print(f'==== {requestId}, {protoId}, {protoMsgReq}, {protoMsgRsp}, {protoData}===')

        if not hasattr(msg_pb2.BattleProtoIds, protoId):
            raise Exception(f"protoId {protoId} not found")
        
        if not hasattr(msg_pb2, protoMsgReq):
            raise Exception(f"protoMsgReq {protoMsgReq} not found")
        
        if not hasattr(msg_pb2, protoMsgRsp):
            raise Exception(f"protoMsgRsp {protoMsgRsp} not found")

        reqValue = getattr(msg_pb2, protoMsgReq)
        reqInstance = reqValue()
        if protoData is not None:
            proto.ParseDict(protoData, reqInstance)

        baseReq = base_pb2.BaseReq()
        baseReq.protoId = msg_pb2.BattleProtoIds.Value(protoId)
        baseReq.requestId = requestId
        if reqInstance is not None:
            baseReq.data = proto.SerializeToString(reqInstance)
        print(baseReq)
        # payload sent to server
        client_payload = proto.sendPayload(baseReq)

        server_payload = mockServer(client_payload)
        return proto.revPayload(server_payload)
    except Exception as e:
        return {"Error": str(e)}


def mockServer(recv_data):
    print("====mockServer====")
    proto = ProtoKlass()

    all_len = len(recv_data)
    if all_len < 4:
        return
    bin_len = decodeLittle(recv_data[:4])
    bin = recv_data[4:]
    print(bin_len, bin)

    baseReq = base_pb2.BaseReq()
    proto.ParseFromString(baseReq, bin)

    baseRsp = base_pb2.BaseRsp()
    baseRsp.protoId =  baseReq.protoId
    baseRsp.responseId = baseReq.requestId
    baseRsp.notifySeqId = next(serverIdGen)
    baseRsp.errorCode = base_pb2.ErrorCode.Value('Err_GmCommondReq')
    # baseRsp.data = 

    # resValue = getattr(msg_pb2, protoMsgRsp)
    # reqInstance = resValue()

    # payload rev from server
    server_payload = proto.sendPayload(baseRsp)

    return server_payload
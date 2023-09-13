import uuid

from flask import Flask, request, session, jsonify, has_request_context, copy_current_request_context
from flask_script import Manager, Server
from functools import wraps
from concurrent.futures import Future, ThreadPoolExecutor
from Core.utils import run_async, remoteUri, remoteTcp, secretKey, logging, ProtoKlass
from clients.wssClient import WssConnector
from clients.tcpClient import TcpConnector

app = Flask(__name__)
app.secret_key = secretKey
manager = Manager(app)

mode = None
uid = None
ws = None # websocket connector
ts = None # tcp socket connector

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
            print(f"mode : {mode}")
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
    reqjson = request.get_json() 
    # ws.PutInMsg(reqjson)
    code = 0
    if 'code' in reqjson:
        code = reqjson['code']

    return await ws.FetchSateDictMsg(code)

import progen.python.todolist_pb2 as TodoList

@app.route('/protos', methods=['GET', 'POST'])
@run_async
async def protos():
    my_list = TodoList.TodoList()
    my_list.owner_id = 1234
    my_list.owner_name = "Tim"

    first_item = my_list.todos.add()
    first_item.state = TodoList.TaskState.Value("TASK_DONE")
    first_item.task = "Test ProtoBuf for Python"
    first_item.due_date = "31.10.2019"

    proto = ProtoKlass()

    bin = proto.SerializeToString(my_list)
    print(bin)
    my_list2 = TodoList.TodoList()
    proto.ParseFromString(my_list2, bin)
    print(my_list2)
    return proto.MessageToJson(my_list)
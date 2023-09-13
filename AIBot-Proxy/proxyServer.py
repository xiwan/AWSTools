import uuid

from flask import Flask, request, session, jsonify, has_request_context, copy_current_request_context
from flask_script import Manager, Server
from functools import wraps
from concurrent.futures import Future, ThreadPoolExecutor
from Core.utils import run_async, remoteUri, secretKey, logging, ProtoKlass
from clients.wssClient import WssConnector

app = Flask(__name__)
app.secret_key = secretKey
manager = Manager(app)

uid = None
ws = None # websocket connector
ts = None # tcp socket connector

@app.before_request
def before_reql(*args, **kwargs):
    global uid, ws
    uid = session.get("sessionid")
    if not uid:
        uid = uuid.uuid1()
        session["sessionid"] = uid

    ws = WssConnector()

    if not ws or not uid:
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

@app.route('/', methods=['GET', 'POST'])
@run_async
async def hello():
    reqjson = request.get_json() 
    ws.PutInMsg(reqjson)
    return await ws.FetchMsg()

@app.route('/init', methods=['GET', 'POST'])
@run_async
async def init():
    reqjson = request.get_json() 
    ws.PutInMsg(reqjson)
    return await ws.FetchMsg()

@app.route('/reset', methods=['GET', 'POST'])
@run_async
async def reset():
    reqjson = request.get_json() 
    ws.PutInMsg(reqjson)
    return await ws.FetchMsg()

@app.route('/action', methods=['GET', 'POST'])
@run_async
async def action():
    reqjson = request.get_json() 
    ws.PutInMsg(reqjson)
    return await ws.FetchMsg()

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

@app.route('/test', methods=['GET', 'POST'])
@run_async
async def test():
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
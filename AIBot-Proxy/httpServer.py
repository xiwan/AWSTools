import uuid

from flask import Flask, request, session, jsonify, has_request_context, copy_current_request_context
from flask_script import Manager
from functools import wraps
from concurrent.futures import Future, ThreadPoolExecutor
from Core.runAsync import run_async, remoteUri, secretKey
from wsClient import ConnectorKls, ConnectorPool

app = Flask(__name__)
app.secret_key = secretKey
manager = Manager(app)
pool = ConnectorPool()

uid = None
ws = None

@app.before_request
def before_reql(*args, **kwargs):
    global uid, ws
    uid = session.get("sessionid")
    if not uid:
        uid = uuid.uuid1()
        session["sessionid"] = uid

    ws = pool.GetConn(str(uid))
    if ws is None:
        ws = ConnectorKls()
        pool.RegConn(uid, ws)
        # pool.BuildConns()

    if not ws or not uid:
        return str(404)
    # finalize the global vars
    uid = session.get("sessionid")
    uid = remoteUri
    ws = pool.GetConn(uid)    
    print(uid, ws)  
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
    ws.PutInMsg(reqjson)
    return await ws.FetchMsg()
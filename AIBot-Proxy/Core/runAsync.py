import logging
import threading
import asyncio
import time
import os

from datetime import date
from flask import Flask, jsonify, has_request_context, copy_current_request_context, request
from flask_script import Manager
from functools import wraps
from concurrent.futures import Future, ThreadPoolExecutor

from configparser import ConfigParser

cfg = ConfigParser()
cfg.read("./env.local.ini")

config = cfg['config']
routeTable = cfg['route']

remoteUri = cfg['config']['remoteUri']
secretKey = cfg['config']['secretKey']
binary = cfg['config']['binary']

logfileName = date.today().strftime('%Y-%m-%d') + "-" +  str(threading.current_thread().ident)
logging.basicConfig(filename=f"./logs/proxy-{logfileName}.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)

def run_async(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        call_result = Future()
        def _run():
            logging.info(f"In [run_async] flask global level: {threading.current_thread().name}")
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(func(*args, **kwargs))
            except Exception as error:
                call_result.set_exception(error)
            else:
                call_result.set_result(result)
            finally:
                loop.close()
 
        loop_executor = ThreadPoolExecutor(max_workers=1)
        if has_request_context():
            _run = copy_current_request_context(_run)
        loop_future = loop_executor.submit(_run)
        loop_future.result()
        return call_result.result()
 
    return _wrapper


def decodeLittle(CSID): 
  return int.from_bytes(CSID, byteorder='little')

def decodeBig(CSID): 
  return int.from_bytes(CSID, byteorder='big')

def getbyteLitte(CSID): 
  return CSID.to_bytes(4, byteorder='little')

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner
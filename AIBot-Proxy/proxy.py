
import time
import threading
import sys
import argparse

from wsHandler import CustomThread
from httpServer import app, Server, run_async, remoteUri, logging
from wssClient import WssConnector

# @manager.command
# def i_say(arg, num):
#     print(arg * int(num))

def wssConnector(host, port):
    s = time.time()
    print(f"In [{threading.current_thread().name}] flask global id: {str(threading.current_thread().ident)}")

    wss = WssConnector()

    httpRev1 = CustomThread(app.run, (host, port,))
    wsAdaptor = CustomThread(wss.OnConnect, (remoteUri,))

    wsAdaptor.start()
    httpRev1.start()

    wsAdaptor.join()
    httpRev1.join()
    logging.info("Exit Main Program")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='proxy server command-line options')
    parser.add_argument('--mode', type=str, help='mode value: wss server or tcp server', default='wss')
    parser.add_argument('--host', type=str, help='host address: 0.0.0.0 or localhost', required=True, default='localhost')
    parser.add_argument('--port', type=int, help='host port number: 5000', required=True, default='5000')

    args = parser.parse_args()

    if args.mode == 'wss' or args.mode == 'ws':
        wssConnector(args.host, args.port)
    elif args.mode == 'tcp':
        print('tcp connector')
    else:
        print('not a valid mode')

    pass






 




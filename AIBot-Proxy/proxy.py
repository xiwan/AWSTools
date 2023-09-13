
import time
import threading
import sys
import argparse

from Core.utils import CustomThread
from proxyServer import app, Server, run_async, remoteUri, remoteTcp, logging
from clients.wssClient import WssConnector
from clients.tcpClient import TcpConnector

def wssConnector(host, port, mode=None):
    print(f"In [{threading.current_thread().name}] flask global id: {str(threading.current_thread().ident)}, time: {time.time()}")
    wss = WssConnector()
    #app.config['SERVER_NAME'] = f"{host}:{port}"
    app.config['SERVER_MODE'] = mode
    httpRev1 = CustomThread(lambda host, port: app.run(host=host, port=port), (host, port, ))
    wsAdaptor = CustomThread(lambda remoteUri: wss.OnConnect(remoteUri), (remoteUri,))

    wsAdaptor.start()
    httpRev1.start()

    wsAdaptor.join()
    httpRev1.join()

def tcpConnector(host, port, mode=None):
    print(f"In [{threading.current_thread().name}] flask global id: {str(threading.current_thread().ident)}, time: {time.time()}")
    tcp = TcpConnector()
    #app.config['SERVER_NAME'] = f"{host}:{port}"
    app.config['SERVER_MODE'] = mode
    httpRev1 = CustomThread( lambda host, port: app.run(host=host, port=port), (host, port, ))
    wsAdaptor = CustomThread( lambda remoteTcp: tcp.OnConnect(remoteTcp), (remoteTcp,))

    wsAdaptor.start()
    httpRev1.start()

    wsAdaptor.join()
    httpRev1.join()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='proxy server command-line options')
    parser.add_argument('--mode', type=str, help='mode value: wss server or tcp server', default='wss')
    parser.add_argument('--host', type=str, help='host address: 0.0.0.0 or localhost', required=True, default='localhost')
    parser.add_argument('--port', type=int, help='host port number: 5000', required=True, default='5000')
    args = parser.parse_args()

    if args.mode == 'wss' or args.mode == 'ws':
        wssConnector(args.host, args.port, args.mode)
    elif args.mode == 'tcp':
        tcpConnector(args.host, args.port, args.mode)
    else:
        print('not a valid mode')

    logging.info("Exit Main Program")
    pass






 




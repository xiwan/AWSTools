
import time
import threading
import sys
import argparse

from Core.utils import CustomThread
from proxyServer import app, run_async, remoteUri, remoteTcp, logging
from clients.wssClient import WssConnector
from clients.tcpClient import TcpConnector
    
def main(host, port, mode=None):
    print(f"In [{threading.current_thread().name}] flask global id: {str(threading.current_thread().ident)}, time: {time.time()}, mode: {mode}")
    app.config['SERVER_MODE'] = mode
    
    if mode == 'wss' or mode == 'ws':
        wss = WssConnector()
        adaptor = CustomThread(lambda remoteUri: wss.OnConnect(remoteUri), (remoteUri,))
    elif mode == 'tcp':
        tcp = TcpConnector()
        adaptor = CustomThread( lambda remoteTcp: tcp.OnConnect(remoteTcp), (remoteTcp,))
    else:
        print('not a valid mode')
        return
    
    httpRev1 = CustomThread( lambda host, port: app.run(host=host, port=port), (host, port, ))

    adaptor.start()
    httpRev1.start()

    adaptor.join()
    httpRev1.join()

    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='proxy server command-line options')
    parser.add_argument('--mode', type=str, help='mode value: wss server or tcp server', default='wss')
    parser.add_argument('--host', type=str, help='host address: 0.0.0.0 or localhost', required=True, default='localhost')
    parser.add_argument('--port', type=int, help='host port number: 5000', required=True, default='5000')
    args = parser.parse_args()

    main(args.host, args.port, args.mode)

    logging.info("Exit Main Program")
    pass






 




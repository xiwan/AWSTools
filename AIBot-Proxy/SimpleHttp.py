import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from wsClient import ConnectorKls

data = {'result': 'this is a test'}
host = ('0.0.0.0', 5000)
ws = ConnectorKls()

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        datas = self.rfile.read(int(self.headers['content-length']))

        print('headers', self.headers)
        print("do post:", self.path, self.client_address, datas.decode('utf-8'))




# if __name__ == '__main__':
#     server = HTTPServer(host, HttpHandler)
#     print("Starting server, listen at: %s:%s" % host)
#     server.serve_forever()

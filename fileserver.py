#!/usr/bin/python
import BaseHTTPServer
import os
import ssl

HOST = '10.200.32.131'
PORT = 4443

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_PUT(s):
        if 'Session-Id' in s.headers:
            length = int(s.headers['Content-Length'])
            path = "Storage/{}/".format(s.headers['Session-Id'])

            if not os.path.isdir(path):
                os.mkdir(path)

            with open(path + s.headers['File-Name'], "wb") as dst:
                dst.write(s.rfile.read(length))
            s.send_response(200)
            s.end_headers()
        else:
            s.send_response(501)
            s.end_headers()
            s.wfile.write("Method not implemented\r\n")

    def do_GET(s):
        global sessionid
        s.send_response(200)
        s.send_header('Content-type', 'application/octet-stream')

        filepath = "."+s.path
        in_file = open(filepath, "rb")
        data = in_file.read()
        in_file.close()

        s.end_headers()
        s.wfile.write(data)

# Colors
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


if __name__ == '__main__':
    if not os.path.isdir('Storage'):
        os.mkdir('Storage')
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST, PORT), Handler)

    # Ssl implementation
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./Certificate/server.pem', server_side=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('{}\n[!] Server is terminated{}'.format(bcolors.WARNING, bcolors.ENDC))
        httpd.server_close()

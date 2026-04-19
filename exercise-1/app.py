from http.server import *

class GFG(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header('content-type', 'text/html')
        self.end_headers()

        self.wfile.write('Hello from Kubernetes!'.encode())


port = HTTPServer(('', 8080), GFG)

port.serve_forever()

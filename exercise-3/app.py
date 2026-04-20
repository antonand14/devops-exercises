from http.server import HTTPServer, BaseHTTPRequestHandler


class GFG(BaseHTTPRequestHandler):

    def do_GET(self):

        global count
        count += 1
        self.send_response(200)

        self.send_header('content-type', 'text/html')
        self.end_headers()

        self.wfile.write(('Request count: ' + str(count)).encode())


count = 0
port = HTTPServer(('', 8080), GFG)
port.serve_forever()

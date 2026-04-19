from http.server import HTTPServer, BaseHTTPRequestHandler

count = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global count
        count += 1
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Request count: {count}".encode())

HTTPServer(("", 8080), Handler).serve_forever()

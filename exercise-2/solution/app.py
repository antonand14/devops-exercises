import os
from http.server import HTTPServer, BaseHTTPRequestHandler

MESSAGE = os.environ.get("GREETING", "Hello, World!")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(MESSAGE.encode())

HTTPServer(("", 8080), Handler).serve_forever()

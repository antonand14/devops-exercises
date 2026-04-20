import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

request_log = []

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = os.environ["MESSAGE"]
        request_log.append(datetime.utcnow().isoformat())

        payload = {
            "message": message,
            "request_number": len(request_log),
            "last_requests": request_log[-3:],
        }

        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("", 8080), Handler).serve_forever()

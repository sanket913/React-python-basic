import http.server
import socketserver
import json
import os

PORT = int(os.environ.get("PORT", 5000))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                user_message = data.get('message', '')
                print("User said:", user_message)

                # Static response
                response_message = "Hi! I'm a Python bot. You said: " + user_message
            except Exception as e:
                response_message = "Error: " + str(e)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'reply': response_message}), 'utf-8'))
        else:
            self.send_error(404)

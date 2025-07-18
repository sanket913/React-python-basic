import http.server
import socketserver
import os
import json

PORT = 5000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    
    # Handle CORS Preflight for POST requests
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # Only POST /chat supported
    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                # Parse JSON input from frontend
                data = json.loads(body.decode('utf-8'))
                user_message = data.get('message', '')
                print(f"User said: {user_message}")

                # Static response message (can be customized)
                reply = f"Hello! You said: {user_message}"

                response = {'reply': reply}
                response_data = json.dumps(response)
            except Exception as e:
                response_data = json.dumps({'reply': f"Error: {str(e)}"})

            # Send JSON response
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response_data.encode('utf-8'))
        else:
            self.send_error(404)

# Run the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at http://0.0.0.0:{PORT}")
    httpd.serve_forever()

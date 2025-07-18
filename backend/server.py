import http.server
import socketserver
import os
import json
from datetime import datetime

PORT = 5000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode('utf-8'))
                user_message = data.get('message', '').strip()
                print(f"[User] {user_message}")

                # Format time for reply
                timestamp = datetime.now().strftime("%H:%M")

                # Example logic: static response based on input
                if user_message.lower() in ['hi', 'hello']:
                    reply_text = "Hello! How can I help you today?"
                elif user_message.lower() in ['bye', 'exit']:
                    reply_text = "Goodbye! Have a nice day 😊"
                else:
                    reply_text = f"You said: {user_message}"

                response = {
                    "reply": {
                        "sender": "bot",
                        "message": reply_text,
                        "time": timestamp
                    }
                }

                response_data = json.dumps(response)

            except Exception as e:
                response_data = json.dumps({
                    "reply": {
                        "sender": "bot",
                        "message": f"Error: {str(e)}",
                        "time": datetime.now().strftime("%H:%M")
                    }
                })

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

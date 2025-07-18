import http.server
import socketserver
import json
from datetime import datetime
import google.generativeai as genai  # Gemini import

# ========== Gemini Configuration ==========
GOOGLE_API_KEY = "AIzaSyBwY8Sb0b2nOKM7e-7-7QI8QxfPSStjSZc"  # Use your actual key here
genai.configure(api_key=GOOGLE_API_KEY)

# Load the model
model = genai.GenerativeModel("gemini-pro")

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

                # Call Gemini API
                gemini_response = model.generate_content(user_message)
                bot_reply = gemini_response.text.strip()

                # Prepare response
                timestamp = datetime.now().strftime("%H:%M")
                response = {
                    "reply": {
                        "sender": "bot",
                        "message": bot_reply,
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
    print(f"✅ Server running at http://0.0.0.0:{PORT}")
    httpd.serve_forever()

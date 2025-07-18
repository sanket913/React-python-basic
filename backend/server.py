import http.server
import socketserver
import subprocess
import os

PORT = int(os.environ.get("PORT", 5000))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/run-script':
            try:
                output = subprocess.check_output(['python', 'hello.py'])
                message = output.decode('utf-8').strip()
            except Exception as e:
                message = str(e)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(f'{{"message": "{message}"}}', 'utf-8'))
        else:
            self.send_error(404)

# Run server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at http://0.0.0.0:{PORT}")
    httpd.serve_forever()

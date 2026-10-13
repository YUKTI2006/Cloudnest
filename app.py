import os
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")

class App(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        message = f"""
        <h1>Hello from CloudNest Python App!</h1>
        <p>Database Host: {DB_HOST}</p>
        <p>Database Name: {DB_NAME}</p>
        """

        self.wfile.write(message.encode())

HTTPServer(("0.0.0.0", 5000), App).serve_forever()

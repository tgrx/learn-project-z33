import os
import socketserver
from http.server import SimpleHTTPRequestHandler

PORT = int(os.getenv("PORT", 8000))


class MyHandler(SimpleHTTPRequestHandler):
    pass


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)


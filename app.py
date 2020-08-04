import socketserver

import settings
from server import MyHttp

if __name__ == "__main__":
    with socketserver.TCPServer(("", settings.PORT), MyHttp) as httpd:
        print("it works")
        httpd.serve_forever(poll_interval=1)

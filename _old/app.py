import socketserver

from framework import settings
from framework.server import MyHttp


def server_greet():
    print()
    print("*" * 40, "run", "*" * 40)
    print(f"PROJECT_DIR: \t{settings.PROJECT_DIR}")
    print(f"SERVER:      \thttp://localhost:{settings.PORT}")
    print("*" * 85)
    print()


if __name__ == "__main__":
    with socketserver.TCPServer(("", settings.PORT), MyHttp) as httpd:
        server_greet()
        try:
            httpd.serve_forever(poll_interval=0.4)
        finally:
            httpd.shutdown()

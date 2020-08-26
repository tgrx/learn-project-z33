import traceback
from http.server import SimpleHTTPRequestHandler

import settings
from custom_types import Endpoint
from errors import MethodNotAllowed
from errors import NotFound
from utils import get_content_type
from utils import read_static
from utils import to_bytes


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        endpoint = Endpoint.from_path(self.path)
        content_type = get_content_type(endpoint.file_name)

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/0/": [self.handle_zde, []],
            "/hello/": [self.handle_hello, []],
            "/i/": [self.handle_static, [f"images/{endpoint.file_name}", content_type]],
            "/s/": [self.handle_static, [f"styles/{endpoint.file_name}", content_type]],
        }

        try:
            handler, args = endpoints[endpoint.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_hello(self):
        content = f"""
        <html>
        <head><title>Hello Page</title></head>
        <body>
        <h1>Hello world!</h1>
        <p>path: {self.path}</p>
        </body>
        </html>
        """

        self.respond(content)

    def handle_zde(self):
        x = 1 / 0
        print(x)

    def handle_static(self, file_path, content_type):
        content = read_static(file_path)
        self.respond(content, content_type=content_type)

    def handle_404(self):
        msg = """CHECK YOU"""
        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        msg = traceback.format_exc()
        self.respond(msg, code=500, content_type="text/plain")

    def respond(self, message, code=200, content_type="text/html"):
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()
        self.wfile.write(payload)

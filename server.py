import traceback
from http.server import SimpleHTTPRequestHandler

import settings
from errors import MethodNotAllowed
from errors import NotFound
from utils import normalize_path
from utils import read_static
from utils import to_bytes


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = normalize_path(self.path)

        handlers = {
            "/": self.handle_root,
            "/hello/": self.handle_hello,
            "/style/": self.handle_style,
            "/logo/": self.handle_logo,
            "/0/": self.handle_zde,
        }

        try:
            handler = handlers[path]
            handler()
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_root(self):
        return super().do_GET()

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

    def handle_style(self):
        css = read_static("styles/style.css")
        self.respond(css, content_type="text/css")

    def handle_logo(self):
        image = read_static("images/logo.svg")
        self.respond(image, content_type="image/svg+xml")

    def handle_404(self):
        msg = """NOT FOUND!!!!!!!!"""

        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        self.respond(traceback.format_exc(), code=500, content_type="text/plain")

    def respond(self, message, code=200, content_type="text/html"):
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()
        self.wfile.write(payload)

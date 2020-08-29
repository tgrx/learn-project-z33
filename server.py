import traceback
from datetime import datetime
from http.server import SimpleHTTPRequestHandler

import settings
from custom_types import Url
from errors import MethodNotAllowed
from errors import NotFound
from utils import get_content_type
from utils import get_user_data
from utils import read_static
from utils import to_bytes


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        url = Url.from_path(self.path)
        content_type = get_content_type(url.file_name)

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/0/": [self.handle_zde, []],
            "/hello/": [self.handle_hello, [url]],
            "/i/": [self.handle_static, [f"images/{url.file_name}", content_type]],
            "/s/": [self.handle_static, [f"styles/{url.file_name}", content_type]],
        }

        try:
            handler, args = endpoints[url.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_hello(self, url):
        user = get_user_data(url.query_string)
        year = datetime.now().year - user.age

        content = f"""
        <html>
        <head><title>Study Project Z33 :: Hello</title></head>
        <body>
        <h1>Hello {user.name}!</h1>
        <h1>You was born at {year}!</h1>
        <p>path: {self.path}</p>
        
        <form>
            <label for="name-id">Your name:</label>
            <input type="text" name="name" id="name-id">

            <label for="age-id">Your age:</label>
            <input type="text" name="age" id="age-id">

            <button type="submit" id="greet-button-id">Greet</button>
        </form>
        
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

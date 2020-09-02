import traceback
from datetime import datetime
from http.server import SimpleHTTPRequestHandler

from custom_types import HttpRequest
from errors import MethodNotAllowed
from errors import NotFound
from settings import STORAGE_DIR
from utils import get_user_data
from utils import read_static
from utils import to_bytes


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.dispatch("get")

    def do_POST(self):
        self.dispatch("post")

    def dispatch(self, http_method):
        req = HttpRequest.from_path(self.path, method=http_method)

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/0/": [self.handle_zde, []],
            "/hello/": [self.handle_hello, [req]],
            "/hello-update/": [self.handle_hello_update, [req]],
            "/i/": [self.handle_static, [f"images/{req.file_name}", req.content_type]],
            "/s/": [self.handle_static, [f"styles/{req.file_name}", req.content_type]],
        }

        try:
            handler, args = endpoints[req.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def get_request_payload(self) -> str:
        content_length_in_str = self.headers.get("content-length", 0)
        content_length = int(content_length_in_str)

        if not content_length:
            return ""

        payload_in_bytes = self.rfile.read(content_length)
        payload = payload_in_bytes.decode()
        return payload

    def get_user_qs_from_file(self):
        qs_file = STORAGE_DIR / "xxx.txt"
        if not qs_file.is_file():
            return ""

        with qs_file.open("r") as src:
            content = src.read()

        if isinstance(content, bytes):
            content = content.decode()

        return content

    def save_user_qs_to_file(self, query: str):
        qs_file = STORAGE_DIR / "xxx.txt"

        with qs_file.open("w") as dst:
            dst.write(query)

    def handle_hello(self, request: HttpRequest):
        if request.method != "get":
            raise MethodNotAllowed

        query_string = self.get_user_qs_from_file()

        user = get_user_data(query_string)

        year = datetime.now().year - user.age

        content = f"""
        <html>
        <head><title>Study Project Z33 :: Hello</title></head>
        <body>
        <h1>Hello {user.name}!</h1>
        <h1>You was born at {year}!</h1>
        <p>path: {self.path}</p>
        
        <form method="post" action="/hello-update">
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

    def handle_hello_update(self, request: HttpRequest):
        if request.method != "post":
            raise MethodNotAllowed

        qs = self.get_request_payload()
        self.save_user_qs_to_file(qs)
        self.redirect("/hello")

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
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, to):
        self.send_response(302)
        self.send_header("Location", to)
        self.end_headers()

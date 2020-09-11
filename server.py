import traceback
from datetime import date
from http.server import SimpleHTTPRequestHandler

from jinja2 import Template

from consts import CSS_CLASS_ERROR
from consts import USERS_DATA
from custom_types import HttpRequest
from custom_types import User
from errors import MethodNotAllowed
from errors import NotFound
from utils import read_static
from utils import to_bytes
from utils import to_str


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
            "/hello-reset/": [self.handle_hello_reset, [req]],
            "/i/": [self.handle_static, [f"images/{req.file_name}", req.content_type]],
            "/s/": [self.handle_static, [f"styles/{req.file_name}", req.content_type]],
        }

        try:

            try:
                handler, args = endpoints[req.normal]
            except KeyError:
                raise NotFound

            handler(*args)
        except NotFound:
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_hello(self, request: HttpRequest):
        if request.method != "get":
            raise MethodNotAllowed

        query = self.load_user_data()
        user = User.build(query)

        content = self.render_hello_page(user, user)

        self.respond(content)

    def handle_hello_update(self, request: HttpRequest):
        if request.method != "post":
            raise MethodNotAllowed

        form_data = self.get_form_data()
        new_user = User.build(form_data)

        if not new_user.errors:
            self.save_user_data(form_data)
            self.redirect("/hello")
            return

        saved_data = self.load_user_data()
        saved_user = User.build(saved_data)

        hello_page = self.render_hello_page(new_user, saved_user)

        self.respond(hello_page)

    def handle_hello_reset(self, request: HttpRequest):
        if request.method != "post":
            raise MethodNotAllowed

        self.reset_user_data()
        self.redirect("/hello/")

    def render_hello_page(self, new_user: User, saved_user: User) -> str:
        css_class_for_name = css_class_for_age = ""
        label_for_name = "Your name: "
        label_for_age = "Your age: "

        age_new = age_saved = saved_user.age
        name_new = name_saved = saved_user.name

        year = date.today().year - age_saved

        if new_user.errors:
            if "name" in new_user.errors:
                error = new_user.errors["name"]
                label_for_name = f"ERROR: {error}"
                css_class_for_name = CSS_CLASS_ERROR

            if "age" in new_user.errors:
                error = new_user.errors["age"]
                label_for_age = f"ERROR: {error}"
                css_class_for_age = CSS_CLASS_ERROR

            name_new = new_user.name
            age_new = new_user.age

        html = read_static("hello.html").decode()
        template = Template(html)

        context = {
            "age_new": age_new or "",
            "label_for_age": label_for_age,
            "label_for_name": label_for_name,
            "name_new": name_new or "",
            "name_saved": name_saved or "",
            "class_for_age": css_class_for_age,
            "class_for_name": css_class_for_name,
            "year": year,
            "fdsfdsfds": 2354234532,
        }

        content = template.render(**context)

        return content

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

    def get_form_data(self) -> str:
        content_length_as_str = self.headers.get("content-length", 0)
        content_length = int(content_length_as_str)

        if not content_length:
            return ""

        payload_as_bytes = self.rfile.read(content_length)
        payload = to_str(payload_as_bytes)

        return payload

    @staticmethod
    def load_user_data() -> str:
        if not USERS_DATA.is_file():
            return ""

        with USERS_DATA.open("r") as src:
            data = src.read()

        data = to_str(data)

        return data

    @staticmethod
    def save_user_data(data: str) -> None:
        with USERS_DATA.open("w") as dst:
            dst.write(data)

    @classmethod
    def reset_user_data(cls) -> None:
        cls.save_user_data("")

import traceback
from http.server import SimpleHTTPRequestHandler

from framework.custom_types import HttpRequest
from framework.custom_types import HttpResponse
from framework.errors import HttpControl
from framework.errors import MethodNotAllowed
from framework.errors import NotFound
from framework.utils import to_bytes
from framework.utils import to_str
from urls import urlpatterns


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.dispatch("get")

    def do_POST(self):
        self.dispatch("post")

    def dispatch(self, http_method):
        try:
            request = HttpRequest.build(
                url=self.path,
                method=http_method,
                headers=dict(self.headers.items()),
                form_data=self.get_form_data(),
            )
            handler = self.get_handler(request)
            response = handler(request)
            self.respond(response)
        except HttpControl as ctl:
            self.respond(ctl.response)
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def get_handler(self, request: HttpRequest):
        if request.path not in urlpatterns:
            raise NotFound(f"Path {request.path} was not found on server")

        handler = urlpatterns[request.path]
        return handler

    def get_form_data(self) -> str:
        content_length_as_str = self.headers.get("Content-Length", 0)
        content_length = int(content_length_as_str)

        if not content_length:
            return ""

        payload_as_bytes = self.rfile.read(content_length)
        payload = to_str(payload_as_bytes)

        return payload

    def handle_405(self) -> None:
        msg = "Method not allowed"
        response = HttpResponse(status_code=405, body=msg, content_type="text/plain")
        self.respond(response)

    def handle_500(self) -> None:
        msg = traceback.format_exc()
        response = HttpResponse(status_code=500, body=msg, content_type="text/plain")
        self.respond(response)

    def respond(self, response: HttpResponse) -> None:
        payload = to_bytes(response.body or "")

        self.send_response(response.status_code)
        self.send_header("Content-Type", response.content_type)
        self.send_header("Content-Length", str(len(payload)))
        for h, v in (response.headers or {}).items():
            self.send_header(h, v)
        self.end_headers()
        if payload:
            self.wfile.write(payload)

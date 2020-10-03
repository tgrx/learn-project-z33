from framework.custom_types import HttpRequest
from framework.custom_types import HttpResponse
from framework.errors import MethodNotAllowed
from framework.utils import render_html


def index(request: HttpRequest) -> HttpResponse:
    if request.method != "get":
        raise MethodNotAllowed

    html = render_html("index.html")

    return HttpResponse(body=html)

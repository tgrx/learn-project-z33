from functools import wraps
from typing import Callable
from typing import Optional

from framework.custom_types import HttpRequest
from framework.custom_types import HttpResponse
from framework.errors import NotFound
from framework.settings import STATIC_DIR


def handle_static_from_prefix(prefix: str) -> Callable:
    @wraps(handle_static)
    def handler(request: HttpRequest):
        return handle_static(request, prefix)

    return handler


def handle_static(request: HttpRequest, prefix: Optional[str] = None) -> HttpResponse:
    static_path = STATIC_DIR
    if prefix:
        static_path /= prefix
    if request.file_name:
        static_path /= request.file_name

    if not static_path.is_file():
        log = (
            f"file {static_path.resolve().as_posix()},"
            f" requested by path {request.path},"
            f"was not found on server"
        )
        raise NotFound(log)

    with static_path.open("rb") as src:
        content = src.read()

    response = HttpResponse(body=content, content_type=request.content_type)
    return response

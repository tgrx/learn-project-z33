from typing import NoReturn

from framework.custom_types import HttpRequest
from framework.errors import MethodNotAllowed
from framework.errors import Redirect
from framework.utils import get_theme
from framework.utils import switch_theme


def switch(request: HttpRequest) -> NoReturn:
    if request.method != "post":
        raise MethodNotAllowed

    current_theme = get_theme(request.session)
    new_theme = switch_theme(current_theme)
    request.session["theme"] = new_theme

    raise Redirect("/hello", headers=request.session.headers)

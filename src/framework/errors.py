import dataclasses
from typing import Dict
from typing import Optional

from framework.custom_types import HttpResponse


class MethodNotAllowed(RuntimeError):
    pass


class HttpControl(Exception):
    code = 400

    @property
    def response(self):
        message = self.args[0] if self.args else None

        return HttpResponse(
            status_code=self.code,
            body=message,
        )


class Redirect(HttpControl):
    code = 302

    def __init__(
        self, to: str, /, headers: Optional[Dict] = None, body: Optional[str] = None
    ):
        self.__body = body
        self.__headers = headers or {}
        self.__headers.update({"Location": to})

    @property
    def response(self):
        original = super().response

        headers = original.headers or {}
        headers.update(self.__headers)

        response = dataclasses.replace(original, headers=headers, body=self.__body)
        return response


class NotFound(HttpControl):
    code = 404

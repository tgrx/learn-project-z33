import mimetypes
from typing import AnyStr
from urllib.parse import parse_qs

import settings
from custom_types import User
from errors import NotFound


def to_bytes(text: AnyStr) -> bytes:
    """
    Safely converts any string to bytes.
    :param text: any string
    :return: bytes
    """

    if isinstance(text, bytes):
        return text

    if not isinstance(text, str):
        err_msg = f"cannot convert {type(text)} to bytes"
        raise ValueError(err_msg)

    result = text.encode()
    return result


def read_static(path: str) -> bytes:
    """
    Reads and returns the content of static file.
    If there is no file, then NotFound exception is raised.
    :param path: path to static content
    :return: bytes of content
    """

    static_obj = settings.STATIC_DIR / path
    if not static_obj.is_file():
        static_path = static_obj.resolve().as_posix()
        err_msg = f"file <{static_path}> not found"
        raise NotFound(err_msg)

    with static_obj.open("rb") as src:
        content = src.read()

    return content


def get_content_type(file_path: str) -> str:
    if not file_path:
        return "text/html"
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type


def get_user_data(qs: str) -> User:
    qp = parse_qs(qs)

    default_names = ["world"]
    default_ages = [0]

    name_values = qp.get("name", default_names)
    age_values = qp.get("age", default_ages)

    name = name_values[0]
    age = int(age_values[0])

    return User(name=name, age=age)

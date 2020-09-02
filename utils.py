import mimetypes
from typing import AnyStr
from urllib.parse import parse_qs

import settings
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
    """
    Calculates content-type against given path. Default is "text/html"
    :param file_path: hypothetical path to file
    :return: content-type value
    """

    if not file_path:
        return "text/html"
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type


def get_user_data(query: str):
    """
    Builds user's data against given query string
    :param query: string
    :return: user's data
    """

    from custom_types import User

    anonymous = User.default()

    try:
        key_value_pairs = parse_qs(query, strict_parsing=True)
    except ValueError:
        return anonymous

    name_values = key_value_pairs.get("name", [anonymous.name])
    name = name_values[0]

    age_values = key_value_pairs.get("age", [anonymous.age])
    age = age_values[0]
    if isinstance(age, str) and age.isdecimal():
        age = int(age)

    return User(name=name, age=age)

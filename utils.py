import os
from http import cookies
from typing import AnyStr
from typing import Dict
from typing import Optional

import settings
from consts import SESSION_AGE
from consts import SESSION_COOKIE
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


def to_str(text: AnyStr) -> str:
    """
    Safely converts any value to str.

    :param text: any string
    :return: str
    """

    result = text

    if not isinstance(text, (str, bytes)):
        result = str(text)

    if isinstance(result, bytes):
        result = result.decode()

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


def get_session_from_headers(headers: Dict) -> Optional[str]:
    """
    Returns session ID value from HTTP request headers.
    Returns None if it is impossible to get the session ID.

    :param headers: dict with HTTP request headers
    :return: session ID or None
    """

    cookie_header = headers.get("Cookie")
    if not cookie_header:
        return None

    jar = cookies.SimpleCookie()
    jar.load(cookie_header)
    if SESSION_COOKIE not in jar:
        return None

    session_morsel = jar[SESSION_COOKIE]
    return session_morsel.value


def generate_new_session() -> str:
    """
    Generates a new session ID value.

    :return: session ID
    """

    session = os.urandom(16).hex()
    return session


def build_session_header(session: str, expires: bool = False) -> str:
    """
    Builds a value for "Set-Cookie" header with session data.

    :param session: session ID
    :param expires: indicates whether to drop cookie or not
    :return: prepared value for "Set-Cookie" header
    """

    jar = cookies.SimpleCookie()
    jar[SESSION_COOKIE] = session
    morsel = jar[SESSION_COOKIE]

    morsel["Domain"] = settings.SITE
    morsel["Path"] = "/"

    max_ages = {
        False: SESSION_AGE,
        True: 0,
    }
    morsel["Max-Age"] = max_ages[expires]

    header = jar[SESSION_COOKIE].OutputString()

    return header


def load_user_data(session: Optional[str]) -> str:
    """
    Loads and returns user's data from its data file.
    User is found by session ID.
    Returns empty string if no session provided.

    :param session: session ID
    :return: user's data
    """

    if not session:
        return ""

    data_file = settings.STORAGE_DIR / f"user_{session}.txt"
    if not data_file.is_file():
        return ""

    with data_file.open("r") as src:
        data = src.read()

    data = to_str(data)

    return data


def store_user_data(session: Optional[str], data: str) -> None:
    """
    Stores user's data in its data file.
    User is found by session ID.
    Does nothing if session ID is not provided.
    Deletes user's data if data value is not provided.

    :param session: session ID
    :param data: user's data
    """

    if not session:
        return

    data_file = settings.STORAGE_DIR / f"user_{session}.txt"
    with data_file.open("w") as dst:
        dst.write(data)


def drop_user_data(session: Optional[str]) -> None:
    """
    Drops saved user's data.
    Does nothing if session ID is not provided.

    :param session: session ID
    """

    if not session:
        return

    store_user_data(session, "")

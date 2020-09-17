import json
import os
from http import cookies
from pathlib import Path
from typing import AnyStr
from typing import Dict
from typing import Optional

import settings
from consts import DEFAULT_THEME
from consts import SESSION_AGE
from consts import SESSION_COOKIE
from consts import THEMES
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


def get_session_from_headers(headers: Optional[Dict]) -> Optional[str]:
    """
    Returns session ID value from HTTP request headers.
    Returns None if it is impossible to get the session ID.

    :param headers: dict with HTTP request headers
    :return: session ID or None
    """

    if not headers:
        return None

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


def switch_theme(current_theme: Optional[str]) -> str:
    """
    Returns a new theme name according to the existing one.
    Assumes default theme if current theme is not provided.

    :param current_theme: current theme
    :return: new theme
    """

    themes = sorted(THEMES)
    themes_fsm = {th1: th2 for th1, th2 in zip(themes, reversed(themes))}

    new_theme = themes_fsm[current_theme or DEFAULT_THEME]

    return new_theme


def load_theme(session: Optional[str]) -> str:
    """
    Loads and returns user's current theme from its session.
    Returns default theme if session is not provided.

    :param session: session ID
    :return: current theme
    """

    data = load_session_data(session)

    return data.get("theme", DEFAULT_THEME)


def store_theme(session: Optional[str], theme: Optional[str]) -> None:
    """
    Stores user's theme in its session data file.
    User is found by session ID.
    Does nothing if session ID is not provided.

    :param session: session ID
    :param theme: user's theme
    """

    if not session:
        return

    session_data = load_session_data(session)

    session_data["theme"] = theme or DEFAULT_THEME

    store_session_data(session, session_data)


def load_profile(session: Optional[str]) -> Optional[str]:
    """
    Loads and returns user's profile from its session.
    User is found by session ID.
    Returns None if session is not provided.

    :param session: session ID
    :return: user's profile (query string)
    """

    data = load_session_data(session)

    return data.get("profile")


def store_profile(session: Optional[str], profile: str) -> None:
    """
    Stores user's profile in its session data file.
    User is found by session ID.
    Does nothing if session ID is not provided.

    :param session: session ID
    :param profile: user's profile
    """

    if not session:
        return

    session_data = load_session_data(session)

    session_data["profile"] = profile

    store_session_data(session, session_data)


def drop_profile(session: Optional[str]) -> None:
    """
    Drops user's saved profile.
    Does nothing if session ID is not provided.

    :param session: session ID
    """

    if not session:
        return

    session_data = load_session_data(session)
    session_data["profile"] = None
    store_session_data(session, session_data)


def load_session_data(session: Optional[str]) -> Dict:
    """
    Loads user's session data from user's data file.
    If session is not provides, returns empty dict.

    :param session: session ID
    :return: dict with session data
    """

    empty_dict = {}

    if not session:
        return empty_dict

    data_file = get_data_file(session)
    if not data_file.is_file():
        return empty_dict

    with data_file.open("r") as src:
        data = json.load(src)

    return data or empty_dict


def store_session_data(
    session: Optional[str], new_session_data: Optional[Dict]
) -> None:
    """
    Stores session data into user's data file.
    Does nothing if no session ID provided.

    :param session: session ID
    :param new_session_data: new session data
    """

    if not session:
        return

    session_data = load_session_data(session)
    session_data.update(new_session_data or {})

    data_file = get_data_file(session)
    with data_file.open("w") as dst:
        json.dump(session_data, dst)


def get_data_file(session: Optional[str]) -> Path:
    """
    Returns path to the user's data file.

    :param session: session ID
    :return: Path
    """

    data_file = (settings.STORAGE_DIR / f"user_{session}.json").resolve()
    return data_file

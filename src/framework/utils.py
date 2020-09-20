from typing import AnyStr
from typing import Dict
from typing import Optional

from jinja2 import Template

from framework import settings
from framework.consts import DEFAULT_THEME
from framework.consts import THEMES
from framework.errors import NotFound
from framework.sessions import Session
from framework.settings import STATIC_DIR


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


def get_theme(session: Session) -> str:
    """
    Loads and returns user's current theme from its session.
    Returns default theme if session is not provided.

    :param session: session ID
    :return: current theme
    """

    theme = session.get("theme", DEFAULT_THEME)
    return theme


def render_html(template: str, context: Optional[Dict] = None) -> str:
    template_file = (STATIC_DIR / template).resolve()
    with template_file.open("r") as src:
        template_html = src.read()
    template_obj = Template(template_html)
    html = template_obj.render(**(context or {}))
    return html

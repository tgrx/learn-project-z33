import mimetypes
from itertools import takewhile
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from urllib.parse import parse_qs
from urllib.parse import SplitResult
from urllib.parse import urlsplit

from framework.sessions import Session


class HttpRequest(NamedTuple):
    method: str = "get"
    path: Optional[str] = "/"
    headers: Optional[Dict] = None
    GET: Optional[Dict] = None
    POST: Optional[Dict] = None
    content_type: Optional[str] = None
    session: Optional[Session] = None
    file_name: Optional[str] = None

    @classmethod
    def default(cls):
        return HttpRequest(
            headers={}, GET={}, POST={}, session=Session(), content_type="text/html"
        )

    @classmethod
    def build(
        cls,
        /,
        url: str,
        method: Optional[str] = None,
        headers: Optional[Dict] = None,
        form_data: Optional[str] = None,
    ) -> "HttpRequest":
        if not url:
            return cls.default()

        components = urlsplit(url)
        normal, file_name = cls._url_to_normal_and_file_name(components)
        content_type = cls._guess_content_type(headers, file_name)
        session = Session.from_headers(headers)

        return HttpRequest(
            method=method or "get",
            path=normal,
            headers=headers or {},
            GET=parse_qs(components.query or ""),
            POST=parse_qs(form_data or ""),
            content_type=content_type,
            session=session,
            file_name=file_name,
        )

    @staticmethod
    def _url_to_normal_and_file_name(components: SplitResult) -> Tuple:
        segments = tuple(filter(bool, components.path.split("/")))
        non_file_segments = takewhile(lambda part: "." not in part, segments)

        compiled = "/".join(non_file_segments)
        normalized = f"/{compiled}/" if compiled not in {"", "/"} else "/"

        last = segments[-1] if segments else ""
        file_name = last if "." in last else None

        return normalized, file_name

    @staticmethod
    def _guess_content_type(headers: Optional[Dict], file_name: Optional[str]) -> str:
        headers = headers or {}
        if "Content-Type" in headers:
            content_type = headers["Content-Type"]
        elif file_name:
            content_type, _ = mimetypes.guess_type(file_name)
        else:
            content_type = "text/html"
        return content_type

from itertools import takewhile
from typing import NamedTuple
from typing import Optional
from urllib.parse import urlsplit

from utils import get_content_type


class HttpRequest(NamedTuple):
    method: str
    original: str
    normal: str
    file_name: Optional[str] = None
    query_string: Optional[str] = None
    content_type: Optional[str] = None

    @classmethod
    def default(cls):
        return cls(method="get", original="", normal="/")

    @classmethod
    def from_path(cls, path: str, method: str) -> "HttpRequest":
        if not path:
            return cls.default()

        components = urlsplit(path)

        segments = tuple(filter(bool, components.path.split("/")))
        non_file_segments = takewhile(lambda part: "." not in part, segments)

        compiled = "/".join(non_file_segments)
        normal = f"/{compiled}/" if compiled not in {"", "/"} else "/"

        last = segments[-1] if segments else ""
        file_name = last if "." in last else None

        content_type = get_content_type(file_name)

        return HttpRequest(
            method=method,
            original=path,
            normal=normal,
            file_name=file_name,
            query_string=components.query or None,
            content_type=content_type,
        )


class User(NamedTuple):
    name: str
    age: int

    @classmethod
    def default(cls):
        return cls(name="anonymous", age=0)

from itertools import takewhile
from typing import NamedTuple
from typing import Optional
from urllib.parse import urlsplit


class Url(NamedTuple):
    original: str
    normal: str
    file_name: Optional[str] = None
    query_string: Optional[str] = None

    @classmethod
    def from_path(cls, path: str) -> "Url":
        if not path:
            from consts import ROOT_URL

            return ROOT_URL

        components = urlsplit(path)

        segments = tuple(filter(bool, components.path.split("/")))
        non_file_segments = takewhile(lambda part: "." not in part, segments)

        compiled = "/".join(non_file_segments)
        normal = f"/{compiled}/" if compiled not in {"", "/"} else "/"

        last = segments[-1] if segments else ""
        file_name = last if "." in last else None

        return Url(
            original=path,
            normal=normal,
            file_name=file_name,
            query_string=components.query or None,
        )


class User(NamedTuple):
    name: str
    age: int

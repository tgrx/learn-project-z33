from itertools import takewhile
from typing import NamedTuple
from typing import Optional


class Endpoint(NamedTuple):
    original: str
    normal: str
    file_name: Optional[str] = None
    query_string: Optional[str] = None

    @classmethod
    def from_path(cls, path: str) -> "Endpoint":
        if not path:
            return Endpoint(original="", normal="/")

        xxx = path.split("?")
        if len(xxx) == 2:
            path, qs = xxx
        else:
            path, qs = xxx[0], None

        parts = tuple(filter(bool, path.split("/")))
        compiled = "/".join(takewhile(lambda part: "." not in part, parts))
        normal = f"/{compiled}/" if compiled not in ("", "/") else "/"

        last = parts[-1] if parts else ""
        file_name = last if "." in last else None

        return Endpoint(
            original=path, normal=normal, file_name=file_name, query_string=qs
        )


class User(NamedTuple):
    name: str
    age: int

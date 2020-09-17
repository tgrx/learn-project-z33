import mimetypes
from itertools import takewhile
from typing import NamedTuple
from typing import Optional
from typing import Union
from urllib.parse import parse_qs
from urllib.parse import urlsplit

from utils import get_session_from_headers
from validatiors import validate_age
from validatiors import validate_name


class HttpRequest(NamedTuple):
    original: str
    normal: str
    method: str = "get"
    file_name: Optional[str] = None
    query_string: Optional[str] = None
    content_type: Optional[str] = "text/html"
    session: Optional[str] = None

    @classmethod
    def default(cls):
        return HttpRequest(original="", normal="/")

    @classmethod
    def build(
        cls, path: str, /, method: Optional[str] = None, headers: Optional = None
    ) -> "HttpRequest":
        if not path:
            return cls.default()

        components = urlsplit(path)

        segments = tuple(filter(bool, components.path.split("/")))
        non_file_segments = takewhile(lambda part: "." not in part, segments)

        compiled = "/".join(non_file_segments)
        normal = f"/{compiled}/" if compiled not in {"", "/"} else "/"

        last = segments[-1] if segments else ""
        file_name = last if "." in last else None

        content_type, _ = mimetypes.guess_type(file_name or "index.html")

        session = get_session_from_headers(headers)

        return HttpRequest(
            content_type=content_type,
            file_name=file_name,
            method=method or "get",
            normal=normal,
            original=path,
            query_string=components.query or None,
            session=session,
        )


class User(NamedTuple):
    errors: Optional[dict] = None

    name: Optional[str] = None
    age: Union[str, int, None] = None

    @classmethod
    def default(cls):
        name = ""
        age = 0
        return User(
            age=age,
            name=name,
        )

    @classmethod
    def build(cls, query: str) -> "User":
        anonymous = cls.default()

        try:
            key_value_pairs = parse_qs(query, strict_parsing=True)
        except ValueError:
            return anonymous

        name_values = key_value_pairs.get("name", [None])
        name = name_values[0]

        age_values = key_value_pairs.get("age", [None])
        age = age_values[0]

        errors = {}

        validations = [
            ("name", validate_name, name),
            ("age", validate_age, age),
        ]

        for field, validation, value in validations:
            try:
                validation(value)
            except ValueError as error:
                errors[field] = str(error)

        if "age" not in errors:
            age = int(age)

        return User(
            age=age,
            name=name,
            errors=errors,
        )

from typing import Dict

import pytest
from framework.custom_types import HttpRequest


@pytest.mark.unit
def test():
    defargs = dict(headers={}, GET={}, POST={}, content_type="text/html")

    data_set = {
        "": HttpRequest(**defargs),
        "/": HttpRequest(**defargs),
        "/images": HttpRequest(**merge(defargs, path="/images/")),
        "/images/": HttpRequest(**merge(defargs, path="/images/")),
        "/images/a": HttpRequest(**merge(defargs, path="/images/a/")),
        "/images/a/": HttpRequest(**merge(defargs, path="/images/a/")),
        "/images/image.jpg": HttpRequest(
            **merge(
                defargs,
                path="/images/",
                file_name="image.jpg",
                content_type="image/jpeg",
            )
        ),
        "/images/image.jpg/": HttpRequest(
            **merge(
                defargs,
                path="/images/",
                file_name="image.jpg",
                content_type="image/jpeg",
            )
        ),
        "/images/x/image.jpg": HttpRequest(
            **merge(
                defargs,
                path="/images/x/",
                file_name="image.jpg",
                content_type="image/jpeg",
            )
        ),
        "/images/x/image.jpg/": HttpRequest(
            **merge(
                defargs,
                path="/images/x/",
                file_name="image.jpg",
                content_type="image/jpeg",
            )
        ),
    }

    for path, expected in data_set.items():
        actual = HttpRequest.build(path)

        compare_requests(actual, expected)


def compare_requests(request_actual: HttpRequest, request_expected: HttpRequest):
    attrs = {
        "content_type",
        "file_name",
        "GET",
        "headers",
        "method",
        "path",
        "POST",
    }

    for attr in attrs:
        expected = getattr(request_expected, attr)
        actual = getattr(request_actual, attr)

        assert actual == expected, (
            f"mismatch at {type(request_expected).__name__}.{attr}:"
            f" expected {expected!r},"
            f" actual {actual!r}"
        )


def merge(default_kwargs: Dict, **kwargs) -> Dict:
    result = {}
    result.update(default_kwargs)
    result.update(kwargs)
    return result

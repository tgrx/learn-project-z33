import pytest

from framework.custom_types import HttpRequest


@pytest.mark.unit
def test():
    data_set = {
        "": HttpRequest(),
        "/": HttpRequest(),
        "/images": HttpRequest(),
        "/images/": HttpRequest(),
        "/images/a": HttpRequest(),
        "/images/a/": HttpRequest(),
        "/images/image.jpg": HttpRequest(),
        "/images/image.jpg/": HttpRequest(),
        "/images/x/image.jpg": HttpRequest(),
        "/images/x/image.jpg/": HttpRequest(),
    }

    for path, expected_endpoint in data_set.items():
        got_endpoint = HttpRequest.build(path)

        assert (
                got_endpoint == expected_endpoint
        ), f"mismatch for `{path}`: expected {expected_endpoint}, got {got_endpoint}"

import pytest

from custom_types import HttpRequest


@pytest.mark.unit
def test():
    data_set = {
        "": HttpRequest(original="", normal="/"),
        "/": HttpRequest(original="/", normal="/"),
        "/images": HttpRequest(original="/images", normal="/images/"),
        "/images/": HttpRequest(original="/images/", normal="/images/"),
        "/images/a": HttpRequest(original="/images/a", normal="/images/a/"),
        "/images/a/": HttpRequest(original="/images/a/", normal="/images/a/"),
        "/images/image.jpg": HttpRequest(
            content_type="image/jpeg",
            file_name="image.jpg",
            normal="/images/",
            original="/images/image.jpg",
        ),
        "/images/image.jpg/": HttpRequest(
            content_type="image/jpeg",
            file_name="image.jpg",
            normal="/images/",
            original="/images/image.jpg/",
        ),
        "/images/x/image.jpg": HttpRequest(
            content_type="image/jpeg",
            file_name="image.jpg",
            normal="/images/x/",
            original="/images/x/image.jpg",
        ),
        "/images/x/image.jpg/": HttpRequest(
            content_type="image/jpeg",
            file_name="image.jpg",
            normal="/images/x/",
            original="/images/x/image.jpg/",
        ),
    }

    for path, expected_endpoint in data_set.items():
        got_endpoint = HttpRequest.build(path)

        assert (
            got_endpoint == expected_endpoint
        ), f"mismatch for `{path}`: expected {expected_endpoint}, got {got_endpoint}"

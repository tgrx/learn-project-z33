import pytest

from custom_types import Url


@pytest.mark.unit
def test_endpoint():
    data_set = {
        "": Url(original="", normal="/"),
        "/": Url(original="/", normal="/"),
        "/images": Url(original="/images", normal="/images/"),
        "/images/": Url(original="/images/", normal="/images/"),
        "/images/a": Url(original="/images/a", normal="/images/a/"),
        "/images/a/": Url(original="/images/a/", normal="/images/a/"),
        "/images/image.jpg": Url(
            original="/images/image.jpg", normal="/images/", file_name="image.jpg"
        ),
        "/images/image.jpg/": Url(
            original="/images/image.jpg/", normal="/images/", file_name="image.jpg"
        ),
        "/images/x/image.jpg": Url(
            original="/images/x/image.jpg", normal="/images/x/", file_name="image.jpg"
        ),
        "/images/x/image.jpg/": Url(
            original="/images/x/image.jpg/", normal="/images/x/", file_name="image.jpg"
        ),
    }

    for path, expected_endpoint in data_set.items():
        got_endpoint = Url.from_path(path)

        assert (
            got_endpoint == expected_endpoint
        ), f"mismatch for `{path}`: expected {expected_endpoint}, got {got_endpoint}"

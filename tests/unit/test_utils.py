import pytest

from errors import NotFound
from utils import normalize_path
from utils import read_static
from utils import to_bytes


@pytest.mark.unit
def test_normalize_path():
    data_set = {
        "": "/",
        "/": "/",
        "hello": "hello/",
        "hello/": "hello/",
    }

    for input_data, expected_data in data_set.items():
        output_data = normalize_path(input_data)

        assert \
            output_data == expected_data, \
            f"path `{input_data}` normalized to `{output_data}`," \
            f" while `{expected_data}` expected"


@pytest.mark.unit
def test_to_bytes():
    input_data_set = ["x", b"x"]
    expected_data_set = [b"x", b"x"]

    for i in range(len(input_data_set)):
        input_data = input_data_set[i]
        expected_data = expected_data_set[i]
        output_data = to_bytes(input_data)

        error = (
            f"failed to convert {input_data!r} to bytes:"
            f" got {output_data!r}, while expected {expected_data!r}"
        )

        assert output_data == expected_data, error


@pytest.mark.unit
def test_read_static():
    content = read_static("test.txt")
    assert content == b"test\n"

    try:
        read_static("xxx")
    except NotFound:
        pass
    else:
        raise AssertionError("file exists")

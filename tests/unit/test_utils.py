import pytest

from errors import NotFound
from utils import read_static
from utils import to_bytes
from utils import to_str


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
def test_to_str():
    input_data_set = ["x", b"x", 1, [], None]
    expected_data_set = ["x", "x", "1", "[]", "None"]

    for i in range(len(input_data_set)):
        input_data = input_data_set[i]
        expected_data = expected_data_set[i]
        output_data = to_str(input_data)

        error = (
            f"failed to convert {input_data!r} to str:"
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

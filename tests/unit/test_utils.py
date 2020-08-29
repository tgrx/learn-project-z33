import pytest

from custom_types import User
from errors import NotFound
from utils import get_user_data
from utils import read_static
from utils import to_bytes


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


@pytest.mark.unit
def test_get_user_data():
    data_set = {
        "": User(name="anonymous", age=0),
        "age": User(name="anonymous", age=0),
        "age=": User(name="anonymous", age=0),
        "name": User(name="anonymous", age=0),
        "name&age": User(name="anonymous", age=0),
        "name&age=": User(name="anonymous", age=0),
        "name=": User(name="anonymous", age=0),
        "name=&age": User(name="anonymous", age=0),
        "name=&age=10": User(name="anonymous", age=10),
        "name=test&age=": User(name="test", age=0),
        "name=test&age=10": User(name="test", age=10),
    }

    for qs, expected in data_set.items():
        got = get_user_data(qs)

        assert got == expected, (
            f"user data mismatch:"
            f" for qs=`{qs}`"
            f" got {got},"
            f" while {expected} expected"
        )

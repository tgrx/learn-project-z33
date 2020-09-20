from urllib.parse import parse_qs

import pytest

from framework.custom_types import User


@pytest.mark.unit
def test():
    data_set = {
        "": User(
            name=None,
            age=None,
            errors={"name": "MUST NOT be empty", "age": "MUST NOT be empty"},
        ),
        "age": User(
            name=None,
            age=None,
            errors={"name": "MUST NOT be empty", "age": "MUST NOT be empty"},
        ),
        "age=": User(
            name=None,
            age=None,
            errors={"name": "MUST NOT be empty", "age": "MUST NOT be empty"},
        ),
        "name": User(
            name=None,
            age=None,
            errors={"name": "MUST NOT be empty", "age": "MUST NOT be empty"},
        ),
        "name&age": User(
            name=None,
            age=None,
            errors={"name": "MUST NOT be empty", "age": "MUST NOT be empty"},
        ),
        "name&age=": User(
            name=None,
            age=None,
            errors={"name": "MUST NOT be empty", "age": "MUST NOT be empty"},
        ),
        "name=": User(
            name=None,
            age=None,
            errors={"name": "MUST NOT be empty", "age": "MUST NOT be empty"},
        ),
        "name=&age": User(
            name=None,
            age=None,
            errors={"name": "MUST NOT be empty", "age": "MUST NOT be empty"},
        ),
        "name=&age=10": User(name=None, age=10, errors={"name": "MUST NOT be empty"}),
        "name=test&age=": User(
            name="test", age=None, errors={"age": "MUST NOT be empty"}
        ),
        "name=test&age=10": User(name="test", age=10, errors={}),
    }

    for qs, expected in data_set.items():
        got = User.build(parse_qs(qs))

        assert got == expected, (
            f"user data mismatch:"
            f" for qs=`{qs}`"
            f" got {got},"
            f" while {expected} expected"
        )

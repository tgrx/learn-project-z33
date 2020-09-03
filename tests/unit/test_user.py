import pytest

from custom_types import User


@pytest.mark.unit
def test():
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
        got = User.from_query(qs)

        assert got == expected, (
            f"user data mismatch:"
            f" for qs=`{qs}`"
            f" got {got},"
            f" while {expected} expected"
        )

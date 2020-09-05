import pytest

from custom_types import User


@pytest.mark.unit
def test():
    data_set = {
        "": User(name="anonymous", age=0),
        "age_valid": User(name="anonymous", age=0),
        "age_valid=": User(name="anonymous", age=0),
        "name_valid": User(name="anonymous", age=0),
        "name_valid&age_valid": User(name="anonymous", age=0),
        "name_valid&age_valid=": User(name="anonymous", age=0),
        "name_valid=": User(name="anonymous", age=0),
        "name_valid=&age_valid": User(name="anonymous", age=0),
        "name_valid=&age_valid=10": User(name="anonymous", age=10),
        "name_valid=test&age_valid=": User(name="test", age=0),
        "name_valid=test&age_valid=10": User(name="test", age=10),
    }

    for qs, expected in data_set.items():
        got = User.build(qs)

        assert got == expected, (
            f"user data mismatch:"
            f" for qs=`{qs}`"
            f" got {got},"
            f" while {expected} expected"
        )

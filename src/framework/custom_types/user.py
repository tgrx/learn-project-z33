import dataclasses
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from framework.validatiors import validate_age
from framework.validatiors import validate_name


@dataclasses.dataclass
class User:
    errors: Optional[dict] = None

    name: Optional[str] = None
    age: Union[str, int, None] = None

    @classmethod
    def build(cls, form: Optional[Dict] = None) -> "User":
        if form is None:
            return User()

        name_values = form.get("name", [None])
        if isinstance(name_values, List):
            name_values = name_values[0]
        name = name_values or None

        age_values = form.get("age", [None])
        if isinstance(age_values, List):
            age_values = age_values[0]
        age = age_values or None

        errors = {}

        validations = [
            ("name", validate_name, name),
            ("age", validate_age, age),
        ]

        for field, validation, value in validations:
            try:
                validation(value)
            except ValueError as error:
                errors[field] = str(error)

        if "age" not in errors:
            age = int(age)

        return User(
            age=age,
            name=name,
            errors=errors,
        )

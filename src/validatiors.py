def validate_name(value: str) -> None:
    if not value:
        raise ValueError("MUST NOT be empty")

    if not value.isalnum() or value.isdigit():
        raise ValueError("MUST contain letters")

    lmin, lmax = 3, 20
    if not lmin <= len(value) <= lmax:
        raise ValueError(f"MUST have length between {lmin}..{lmax} chars")


def validate_age(value: str) -> None:
    if not value:
        raise ValueError("MUST NOT be empty")

    if isinstance(value, str) and not value.isdecimal():
        raise ValueError("MUST contain digits only")

    value = int(value)
    if value <= 0:
        raise ValueError("MUST be positive integer")

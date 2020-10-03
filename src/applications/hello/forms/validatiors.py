def validate_name(value: str) -> None:
    if not value:
        raise ValueError("MUST NOT be empty")

    if not value.isalnum() or value.isdigit():
        raise ValueError("MUST contain letters")

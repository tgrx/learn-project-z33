from typing import Union


def normalize_path(path: str) -> str:
    if not path:
        return "/"

    normalized_path = path

    if normalized_path[-1] != "/":
        normalized_path = f"{normalized_path}/"

    return normalized_path


def to_bytes(text: Union[str, bytes]) -> bytes:
    if isinstance(text, bytes):
        return text

    if not isinstance(text, str):
        raise ValueError(f"cannot convert {type(text)} to bytes")

    result = text.encode()
    return result

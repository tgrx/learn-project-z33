def normalize_path(path: str) -> str:
    if not path:
        return "/"

    normalized_path = path

    if normalized_path[-1] != "/":
        normalized_path = f"{normalized_path}/"

    return normalized_path

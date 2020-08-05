from utils import normalize_path


def test_normalize_path():
    dataset = {
        "": "/",
        "/": "/",
        "/xxx": "/xxx/",
        "/xxx/": "/xxx/",
        "/xxx//": "/xxx//",
        "xxx": "xxx/",
        "xxx/": "xxx/",
    }

    for path, expected in dataset.items():
        got = normalize_path(path)
        assert got == expected, f"path `{path}` normalized to `{got}`, while `{expected}` expected"

import pytest

import settings
from consts import USERS_DATA
from tests.functional.utils import build_chrome


@pytest.yield_fixture(scope="session", autouse=True)
def browser():
    chrome = build_chrome()
    yield chrome
    chrome.close()
    chrome.quit()


@pytest.yield_fixture(scope="session", autouse=True)
def main_css():
    path = settings.STATIC_DIR / "styles" / "main.css"
    with path.open("r") as src:
        yield src.read()


@pytest.yield_fixture(scope="function", autouse=True)
def users_data():
    data = ""
    if USERS_DATA.is_file():
        with USERS_DATA.open("r") as src:
            data = src.read()

    with USERS_DATA.open("w"):
        pass

    yield

    with USERS_DATA.open("w") as dst:
        dst.write(data)

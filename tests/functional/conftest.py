import pytest

from framework import settings
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

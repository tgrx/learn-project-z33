import pytest
from framework import settings

from tests.functional.utils import build_chrome


@pytest.yield_fixture(scope="session", autouse=True)
def browser():
    _browser = build_chrome()

    yield _browser
    _browser.close()
    _browser.quit()


@pytest.yield_fixture(scope="session", autouse=True)
def main_css():
    path = settings.STATIC_DIR / "styles" / "main.css"
    with path.open("r") as src:
        yield src.read()

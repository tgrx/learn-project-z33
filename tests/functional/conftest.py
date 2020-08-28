import pytest

import settings
from tests.functional.utils import build_chrome


@pytest.yield_fixture(scope="session", autouse=True)
def browser():
    bro = build_chrome()
    yield bro
    bro.close()
    bro.quit()


@pytest.yield_fixture(scope="session", autouse=True)
def main_css():
    path = settings.STATIC_DIR / "styles" / "main.css"
    with path.open("r") as src:
        yield src.read()


@pytest.yield_fixture(scope="session", autouse=True)
def logo_svg():
    path = settings.STATIC_DIR / "images" / "logo.svg"
    with path.open("r") as src:
        yield src.read()

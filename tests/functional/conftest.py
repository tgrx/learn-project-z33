import pytest

import settings
from tests.functional.utils import build_chrome


@pytest.yield_fixture(scope="function", autouse=True)
def browser():
    bro = None
    try:
        bro = build_chrome()
        yield bro
    finally:
        if bro:
            bro.close()
            bro.quit()


@pytest.yield_fixture(scope="function", autouse=True)
def main_css():
    path = settings.STATIC_DIR / "styles" / "main.css"
    with path.open("r") as src:
        yield src.read()


@pytest.yield_fixture(scope="function", autouse=True)
def logo_svg():
    path = settings.STATIC_DIR / "images" / "logo.svg"
    with path.open("r") as src:
        yield src.read()

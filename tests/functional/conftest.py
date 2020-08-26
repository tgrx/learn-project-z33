import pytest
from selenium import webdriver

import settings


@pytest.yield_fixture(scope="function", autouse=True)
def chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(10)

    try:
        yield browser
    finally:
        browser.close()
        browser.quit()


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

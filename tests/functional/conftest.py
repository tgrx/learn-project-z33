import pytest
from selenium import webdriver


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

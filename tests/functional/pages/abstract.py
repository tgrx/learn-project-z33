from contextlib import contextmanager
from typing import Union

from selenium.webdriver.android.webdriver import WebDriver as AndroidWebDriver
from selenium.webdriver.blackberry.webdriver import WebDriver as BlackberryWebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.edge.webdriver import WebDriver as EdgeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.ie.webdriver import WebDriver as IeWebDriver
from selenium.webdriver.opera.webdriver import WebDriver as OperaWebDriver
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhantomJsWebDriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

WebDriverT = Union[
    AndroidWebDriver,
    BlackberryWebDriver,
    ChromeWebDriver,
    EdgeWebDriver,
    FirefoxWebDriver,
    IeWebDriver,
    OperaWebDriver,
    PhantomJsWebDriver,
    RemoteWebDriver,
    SafariWebDriver,
]


class PageObject:
    def __init__(self, browser: WebDriverT, url: str):
        self._browser = browser
        self._url = url
        self._browser.get(f"{self._url}")

    @property
    def html(self) -> str:
        return self._browser.page_source

    @property
    def title(self) -> str:
        return self._browser.title

    @contextmanager
    def _resource(self, url: str):
        current_url = self._browser.current_url
        resource_url = f"{self._url}{url}"
        try:
            self._browser.get(resource_url)
            found = WebDriverWait(self._browser, 4).until(
                expected_conditions.url_matches(resource_url)
            )
            assert found
            content = self._browser.page_source
            yield content
        finally:
            self._browser.get(current_url)

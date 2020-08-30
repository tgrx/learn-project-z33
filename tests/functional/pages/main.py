from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .abstract import PageObject


class MainPage(PageObject):
    PROGRESS = (By.CSS_SELECTOR, 'progress#progress')

    @property
    def progress(self) -> WebElement:
        progress = self._browser.find_element(*self.PROGRESS)
        return progress

    @property
    def logo(self):
        with self._resource("/i/logo.svg") as svg:
            return svg

    @property
    def main_css(self):
        with self._resource("/s/main.css") as css:
            return css

from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject
from .abstract import PageResource


class MainPage(PageObject):
    progress = PageElement(By.CSS_SELECTOR, "progress#progress")
    logo = PageResource("/s/images/logo.svg")
    favicon = PageElement(By.CSS_SELECTOR, 'head > link[rel="shortcut icon"]')

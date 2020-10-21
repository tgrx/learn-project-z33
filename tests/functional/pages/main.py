from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject


class MainPage(PageObject):
    progress = PageElement(By.CSS_SELECTOR, "progress#progress")
    favicon = PageElement(By.CSS_SELECTOR, 'head > link[rel="shortcut icon"]')

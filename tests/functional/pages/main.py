from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject
from .abstract import PageResource


class MainPage(PageObject):
    progress = PageElement(By.CSS_SELECTOR, "progress#progress")
    logo = PageResource("/i/logo.svg")
    main_css = PageResource("/s/main.css")

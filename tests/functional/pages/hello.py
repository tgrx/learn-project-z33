from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject


class HelloPage(PageObject):
    button_greet = PageElement(By.CSS_SELECTOR, "button#greet-button-id")
    button_reset = PageElement(By.CSS_SELECTOR, "button#reset-button-id")
    input_name = PageElement(By.CSS_SELECTOR, "input#id_name")
    input_age = PageElement(By.CSS_SELECTOR, "input#id_age")

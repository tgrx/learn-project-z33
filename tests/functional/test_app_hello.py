from datetime import date

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.functional.pages import HelloPage
from tests.functional.utils import screenshot_on_failure

url = "http://localhost:8000/hello"


@pytest.mark.functional
@screenshot_on_failure
def test_get(browser, request):
    page = HelloPage(browser, url)

    validate_title(page)
    validate_structure(page)
    validate_content(page, "Hello anonymous")


@pytest.mark.functional
@screenshot_on_failure
def test_post(browser, request):
    name = "USER"
    age = 10
    year = date.today().year - age

    anon_on_page = "Hello anonymous!"
    name_on_page = f"Hello {name}"
    year_on_page = f"You was born at {year}!"

    page = HelloPage(browser, url)

    validate_structure(page)
    validate_content(page, anon_on_page)

    set_input_name_value(page, name)
    set_input_age_value(page, "")
    submit(page)
    validate_redirect(page, fr"hello/?")
    validate_content(page, anon_on_page)

    set_input_name_value(page, "")
    set_input_age_value(page, str(age))
    submit(page)
    validate_redirect(page, fr"hello/?")
    validate_content(page, anon_on_page)

    set_input_name_value(page, name)
    set_input_age_value(page, str(age))
    submit(page)
    validate_redirect(page, fr"hello/?")
    validate_content(page, name_on_page, year_on_page)

    reset(page)
    validate_redirect(page, fr"hello/?")
    validate_content(page, anon_on_page)


def validate_title(page: HelloPage):
    assert "Z33 :: Hello app" == page.title


def validate_structure(page: HelloPage):
    assert "form" in page.html

    button_submit: WebElement = page.button_greet
    assert button_submit.tag_name == "button"

    button_reset: WebElement = page.button_reset
    assert button_reset.tag_name == "button"

    input_name = page.input_name
    assert input_name.tag_name == "input"

    input_age = page.input_age
    assert input_age.tag_name == "input"


def validate_content(page: HelloPage, *texts):
    html = page.html

    for text in texts:
        assert text in html


def validate_redirect(page: HelloPage, url: str):
    try:
        redirected = WebDriverWait(page.browser, 4).until(
            expected_conditions.url_matches(url)
        )
        assert redirected
    except TimeoutException as err:
        raise AssertionError("no redirect") from err


def set_input_name_value(page: HelloPage, value: str):
    page.input_name.clear()
    if value:
        page.input_name.send_keys(value)


def set_input_age_value(page: HelloPage, value: str):
    page.input_age.clear()
    if value:
        page.input_age.send_keys(value)


def submit(page: HelloPage):
    page.button_greet.send_keys(Keys.RETURN)


def reset(page: HelloPage):
    page.button_reset.send_keys(Keys.RETURN)

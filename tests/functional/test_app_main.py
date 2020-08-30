import pytest

from tests.functional.pages import MainPage
from tests.functional.utils import screenshot_on_failure


@pytest.mark.functional
@screenshot_on_failure
def test(browser, request, main_css):
    page = MainPage(browser, "http://localhost:8000")

    validate_html(page)
    validate_logo(page)
    validate_css(page, main_css)


def validate_html(page: MainPage):
    validate_title(page)
    validate_content(page)


def validate_logo(page: MainPage):
    assert "svg" in page.logo
    assert "Z33" in page.logo


def validate_css(page: MainPage, main_css: str):
    assert main_css in page.main_css


def validate_title(page: MainPage):
    assert "Study Project Z33" in page.title


def validate_content(page: MainPage):
    html = page.html
    assert "Progress" in html
    assert "/s/main.css" in html
    assert "/i/logo.svg" in html

    validate_progress(page)


def validate_progress(page: MainPage):
    assert page.progress
    assert page.progress.tag_name == "progress"
    assert page.progress.text == "42%"
    assert page.progress.get_attribute("max") == "26"
    assert page.progress.get_attribute("value") == "11"

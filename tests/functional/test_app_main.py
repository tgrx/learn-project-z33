import pytest

from tests.functional.pages import MainPage
from tests.functional.utils import screenshot_on_failure

url = "http://localhost:8000"


@pytest.mark.functional
@screenshot_on_failure
def test(browser, request, main_css):
    page = MainPage(browser, url)

    validate_title(page)
    validate_content(page)
    validate_progress(page)
    validate_logo(page)
    validate_css(page, main_css)


def validate_logo(page: MainPage):
    assert "svg" in page.logo
    assert "Z33" in page.logo


def validate_css(page: MainPage, main_css: str):
    page_main_css = page.main_css
    assert main_css in page_main_css


def validate_title(page: MainPage):
    assert "Study Project Z33" in page.title


def validate_content(page: MainPage):
    html = page.html
    assert "Progress" in html


def validate_progress(page: MainPage):
    assert page.progress
    assert page.progress.tag_name == "progress"
    assert page.progress.text == "53%"
    assert page.progress.get_attribute("max") == "26"
    assert page.progress.get_attribute("value") == "14"

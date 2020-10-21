import pytest

from tests.functional.pages import MainPage
from tests.functional.utils import screenshot_on_failure

url = "http://localhost:8000"


@pytest.mark.functional
@screenshot_on_failure
def test(browser, request):
    page = MainPage(browser, url)

    validate_favicon(page)
    validate_title(page)
    validate_content(page)
    validate_progress(page)
    validate_logo(page)


def validate_favicon(page: MainPage):
    assert "s/images/logo.svg" in page.favicon.get_attribute("href")


def validate_logo(page: MainPage):
    assert "svg" in page.logo
    assert "Z33" in page.logo


def validate_title(page: MainPage):
    assert "Z33 :: Home page" == page.title


def validate_content(page: MainPage):
    html = page.html
    assert "Progress" in html


def validate_progress(page: MainPage):
    assert page.progress
    assert page.progress.tag_name == "progress"
    assert page.progress.text == "76%"
    assert page.progress.get_attribute("max") == "26"
    assert page.progress.get_attribute("value") == "20"

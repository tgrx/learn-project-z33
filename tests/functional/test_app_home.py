import pytest

from tests.functional.pages import MainPage
from tests.functional.utils import screenshot_on_failure

url = "http://localhost:8000"


@pytest.mark.functional
@screenshot_on_failure
def test(browser, request):
    page = MainPage(browser, url)

    validate_title(page)
    validate_content(page)
    validate_progress(page)


def validate_title(page: MainPage):
    assert "Z33 :: Home page" == page.title


def validate_content(page: MainPage):
    html = page.html
    assert "Progress" in html


def validate_progress(page: MainPage):
    assert page.progress
    assert page.progress.tag_name == "progress"
    assert page.progress.text == "88%"
    assert page.progress.get_attribute("max") == "26"
    assert page.progress.get_attribute("value") == "23"

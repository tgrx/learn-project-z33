import pytest

url = "http://localhost:8000"


@pytest.mark.functional
def test_html(browser):
    browser.get(f"{url}/")
    assert "Study Project Z33" in browser.title
    assert "Progress" in browser.page_source
    assert "/s/main.css" in browser.page_source
    assert "/i/logo.svg" in browser.page_source

    progress = browser.find_element_by_xpath('//*[@id="progress"]')
    assert progress
    assert progress.tag_name == "progress"
    assert progress.text == "38%"
    assert progress.get_attribute("max") == "26"
    assert progress.get_attribute("value") == "10"


@pytest.mark.functional
def test_logo_svg(browser):
    browser.get(f"{url}/i/logo.svg")
    assert "svg" in browser.page_source
    assert "Z33" in browser.page_source


@pytest.mark.functional
def test_main_css(browser, main_css):
    browser.get(f"{url}/s/main.css")
    assert main_css in browser.page_source

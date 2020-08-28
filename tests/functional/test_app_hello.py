import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

url = "http://localhost:8000/hello"


@pytest.mark.functional
def test_get(browser):
    browser.get(url)

    assert "Study Project Z33 :: Hello" in browser.title

    assert "form" in browser.page_source

    button: WebElement = browser.find_element_by_id("greet-button-id")
    assert button.tag_name == "button"

    input_name = browser.find_element_by_id("name-id")
    assert input_name.tag_name == "input"

    # input_age = browser.find_element_by_id("age")
    # assert input_age.tag_name == "input"

    button = browser.find_element_by_id("greet-button-id")
    assert button.tag_name == "button"


@pytest.mark.functional
def test_get_qs(browser):
    name = "USERNAME"
    name_on_page = f"Hello {name}"

    browser.get(f"{url}?name={name}")

    input_name = browser.find_element_by_id("name-id")
    assert input_name.tag_name == "input"
    assert input_name.text == ""

    assert name_on_page in browser.page_source, f"no '{name_on_page} found on page"


@pytest.mark.functional
def test_get_form(browser):
    name = "USERNAME"
    name_on_page = f"Hello {name}"

    browser.get(f"{url}")

    input_name: WebElement = browser.find_element_by_id("name-id")
    input_name.send_keys(name)

    button: WebElement = browser.find_element_by_id("greet-button-id")
    button.send_keys(Keys.RETURN)

    redirected = WebDriverWait(browser, 10).until(
        expected_conditions.url_matches(r"^.*/hello.*\?.*$")
    )
    assert redirected

    assert browser.current_url.endswith(f"/hello?name={name}")

    assert name_on_page in browser.page_source, f"no '{name_on_page} found on page"

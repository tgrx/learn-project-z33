import pytest


@pytest.mark.functional
def test(chrome):
    chrome.get("http://localhost:8000/")
    assert "XXX" in chrome.title
    assert "YYY" in chrome.page_source

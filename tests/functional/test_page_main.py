import pytest


@pytest.mark.functional
def test(chrome):
    chrome.get("http://localhost:8000/")
    assert "Study Project Z33" in chrome.title
    assert "Progress" in chrome.page_source

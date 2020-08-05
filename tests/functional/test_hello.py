from selenium import webdriver


def test_hello_page():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:8000/hello")
        assert "Hello world!" in driver.title
    finally:
        driver.close()

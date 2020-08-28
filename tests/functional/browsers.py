from selenium import webdriver


def build_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(4)

    return browser

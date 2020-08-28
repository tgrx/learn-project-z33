from datetime import datetime
from functools import wraps

from selenium import webdriver

import settings


def build_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(4)

    return browser


def screenshot_on_failure(test):
    @wraps(test)
    def decorated_test(browser, *args, **kwargs):
        try:
            test(browser, *args, **kwargs)
        except Exception:
            ts = datetime.now().strftime(f"%Y%m%d---%H%M%S")
            fname = f"{test.__name__}---{ts}.png"
            fpath = (settings.SCREENSHOTS_DIR / fname).resolve().as_posix()
            browser.save_screenshot(fpath)
            raise

    return decorated_test

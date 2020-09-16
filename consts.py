from settings import STORAGE_DIR

USERS_DATA = STORAGE_DIR / "users.txt"

CSS_CLASS_ERROR = "error"

SESSION_COOKIE = "xxx_sid"
SESSION_AGE = 7 * 24 * 60 * 60

DEFAULT_THEME = "light"
THEMES = {DEFAULT_THEME, "dark"}

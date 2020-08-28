import os
from pathlib import Path

PORT = int(os.getenv("PORT", 8000))
print(PORT)

CACHE_AGE = 60 * 60 * 24

PROJECT_DIR = Path(__file__).parent.resolve()
STATIC_DIR = PROJECT_DIR / "static"
TESTS_DIR = PROJECT_DIR / "tests"
SCREENSHOTS_DIR = TESTS_DIR / "functional" / "screenshots"

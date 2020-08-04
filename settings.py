import os

PORT = int(os.getenv("PORT", 8000))
print(PORT)

CACHE_AGE = 60 * 60 * 24

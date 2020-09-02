from custom_types import HttpRequest
from custom_types import User

ANONYMOUS_USER = User(name="anonymous", age=0)
ROOT_REQUEST = HttpRequest(method="get", original="", normal="/")

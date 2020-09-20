import dataclasses
from typing import Dict
from typing import Optional


@dataclasses.dataclass
class HttpResponse:
    status_code: int = 200
    content_type: Optional[str] = "text/html"
    headers: Optional[Dict] = None
    body: Optional[str] = None

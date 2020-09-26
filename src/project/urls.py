from pathlib import Path

from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import path


def handler_or_view(request: HttpRequest):
    index_html = Path(__file__).parent.parent.parent / "static" / "index.html"
    with index_html.open("r") as index_html_file:
        html = index_html_file.read()
    return HttpResponse(html, content_type="text/html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", handler_or_view)
]

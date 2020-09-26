from pathlib import Path

from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import path


def view_index(request: HttpRequest):
    index_html = Path(__file__).parent.parent.parent / "static" / "index.html"
    with index_html.open("r") as fp:
        content = fp.read()
    return HttpResponse(content, content_type="text/html")


def view_logo(request: HttpRequest):
    logo = Path(__file__).parent.parent.parent / "static" / "images" / "logo.svg"
    with logo.open("rb") as fp:
        content = fp.read()
    return HttpResponse(content, content_type="image/svg+xml")


def view_css(request: HttpRequest):
    css_file = Path(__file__).parent.parent.parent / "static" / "styles" / "main.css"
    with css_file.open("r") as fp:
        content = fp.read()
    return HttpResponse(content, content_type="text/css")


urlpatterns = [
    path("", view_index),
    path("admin/", admin.site.urls),
    path("i/logo.svg", view_logo),
    path("s/main.css", view_css),
]

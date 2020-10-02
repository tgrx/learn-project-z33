from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from applications.hello.utils import build_context_for_hello


def view_index(request: HttpRequest) -> HttpResponse:
    context = build_context_for_hello(request)

    resp = render(request, "hello/hello.html", context)
    return resp

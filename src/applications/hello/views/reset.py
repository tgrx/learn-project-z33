from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect


def view_reset(request: HttpRequest) -> HttpResponse:
    for user_attr in {"name", "age"}:
        try:
            del request.session[user_attr]
        except KeyError:
            pass

    return redirect("/hello")

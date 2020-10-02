from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect


def view_update(request: HttpRequest) -> HttpResponse:
    name = request.POST.get("name")
    age = request.POST.get("age")

    request.session["name"] = name
    request.session["age"] = age

    return redirect("/hello")

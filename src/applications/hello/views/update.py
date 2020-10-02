from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from applications.hello.forms import HelloForm
from applications.hello.utils import build_context_for_hello


def view_update(request: HttpRequest) -> HttpResponse:
    form = HelloForm(request.POST)

    actions = {
        True: view_hello_form_valid,
        False: view_hello_form_invalid,
    }

    action = actions[form.is_valid()]

    return action(request, form)


def view_hello_form_valid(request: HttpRequest, form: HelloForm) -> HttpResponse:
    request.session["name"] = form.cleaned_data["name"]
    request.session["age"] = form.cleaned_data["age"]

    return redirect("/hello")


def view_hello_form_invalid(request: HttpRequest, form: HelloForm) -> HttpResponse:
    context = build_context_for_hello(request)

    context.update(
        {
            "form": form,
        }
    )

    return render(request, "hello/hello.html", locals())

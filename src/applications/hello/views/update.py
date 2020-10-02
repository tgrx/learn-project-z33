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
    class_for_name = class_for_age = ""
    label_for_name = "Name:"
    label_for_age = "Age:"

    if "name" in form.errors:
        class_for_name = "error"
        label_for_name = form.errors["name"][0]

    if "age" in form.errors:
        class_for_age = "error"
        label_for_age = form.errors["age"][0]

    context = build_context_for_hello(request)

    context.update({
        "class_for_name": class_for_name,
        "label_for_name": label_for_name,
        "class_for_age": class_for_age,
        "label_for_age": label_for_age,
        "form": form,
    })

    return render(request, "hello/hello.html", locals())

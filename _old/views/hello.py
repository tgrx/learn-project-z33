from dataclasses import asdict
from datetime import date
from typing import Dict
from typing import NoReturn
from typing import Union

from framework.consts import CSS_CLASS_ERROR
from framework.custom_types import HttpRequest
from framework.custom_types import HttpResponse
from framework.custom_types import User
from framework.errors import MethodNotAllowed
from framework.errors import Redirect
from framework.utils import get_theme
from framework.utils import render_html


def index(request: HttpRequest) -> HttpResponse:
    if request.method != "get":
        raise MethodNotAllowed

    profile_saved = request.session.get("profile")
    user_saved = User.build(profile_saved)

    context = _build_context(request, user_new=user_saved, user_saved=user_saved)

    html = render_html("hello.html", context)
    return HttpResponse(status_code=200, body=html)


def update(request: HttpRequest) -> Union[HttpResponse, NoReturn]:
    if request.method != "post":
        raise Redirect("/hello")

    user_new = User.build(request.POST)
    profile_saved = request.session.get("profile", {})

    if not user_new.errors:
        profile_new = asdict(user_new)
        profile_saved.view_update(profile_new)
        request.session["profile"] = profile_saved
        raise Redirect("/hello", headers=request.session.headers)

    user_saved = User.build(profile_saved)

    context = _build_context(request, user_new=user_new, user_saved=user_saved)

    html = render_html("hello.html", context)
    return HttpResponse(status_code=400, body=html)


def reset(request: HttpRequest) -> NoReturn:
    if request.method != "post":
        raise Redirect("/hello")

    request.session["profile"] = None
    raise Redirect("/hello", headers=request.session.headers)


def _build_context(
    request,
    /,
    user_saved,
    user_new,
) -> Dict:
    css_class_for_name = css_class_for_age = ""
    label_for_name = "Your name: "
    label_for_age = "Your age: "

    age_saved = user_saved.age
    name_saved = user_saved.name

    year = date.today().year - age_saved if age_saved is not None else None

    errors = user_new.errors or {}

    if error := errors.get("name", None):
        label_for_name = f"ERROR: {error}"
        css_class_for_name = CSS_CLASS_ERROR

    if error := errors.get("age", None):
        label_for_age = f"ERROR: {error}"
        css_class_for_age = CSS_CLASS_ERROR

    name_new = user_new.name
    age_new = user_new.age

    theme = get_theme(request.session)

    context = {
        "age_new": age_new or "",
        "class_for_age": css_class_for_age,
        "class_for_name": css_class_for_name,
        "label_for_age": label_for_age,
        "label_for_name": label_for_name,
        "name_new": name_new or "",
        "name_saved": name_saved or "",
        "new_user": user_new,
        "saved_user": user_saved,
        "theme": theme,
        "year": year,
    }

    return context

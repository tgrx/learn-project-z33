from datetime import date
from typing import Dict

from django.http import HttpRequest

from applications.hello.forms import HelloForm


def build_context_for_hello(request: HttpRequest) -> Dict:
    name_saved = request.session.get("name")
    age_saved = request.session.get("age")

    age_new = ""
    name_new = ""
    year = None

    if age_saved:
        year = date.today().year - int(age_saved)
        age_new = age_saved

    if name_saved:
        name_new = name_saved

    form = HelloForm(
        initial=dict(
            name=name_new,
            age=age_new,
        )
    )

    context = {
        "age_new": age_new,
        "age_saved": age_saved,
        "form": form,
        "name_new": name_new,
        "name_saved": name_saved or "anonymous",
        "theme": "dark",
        "year": year,
    }

    return context

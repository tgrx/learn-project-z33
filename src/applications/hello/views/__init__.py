from django.urls import reverse_lazy
from django.views.generic import FormView

from .index import view_index
from .reset import view_reset
from .update import view_update
from ..forms import HelloForm


class HelloView(FormView):
    template_name = "hello/hello.html"
    form_class = HelloForm
    success_url = reverse_lazy("hello:index")

    def form_valid(self, form):
        self.request.session["name"] = form.cleaned_data["name"]
        self.request.session["age"] = form.cleaned_data["age"]

        return super().form_valid(form)

    def get_initial(self):
        data = {
            "name": self.request.session.get("name"),
            "age": self.request.session.get("age"),
        }

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["name_saved"] = self.request.session.get("name") or "anon"
        context["year"] = self.request.session.get("age")

        return context

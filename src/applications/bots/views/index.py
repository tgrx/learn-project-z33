from django.urls import reverse_lazy
from django.views.generic import ListView


class IndexView(ListView):
    template_name = "bots/index.html"

    def get_queryset(self):
        bots = [
            {
                "name": "Telegram Bot",
                "url": reverse_lazy("bots:register-bot-telegram"),
            },
        ]

        return bots

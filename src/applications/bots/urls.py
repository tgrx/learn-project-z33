from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from applications.bots.apps import BotsConfig
from applications.bots.views import TelegramBotView
from applications.bots.views.index import IndexView

app_name = BotsConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tg/", csrf_exempt(TelegramBotView.as_view()), name="bot-telegram"),
    path("tg/register/", TelegramBotView.register, name="register-bot-telegram"),
]

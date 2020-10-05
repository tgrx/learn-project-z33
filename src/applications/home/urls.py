from django.urls import path

from applications.home.apps import HomeConfig
from applications.home.views import IndexView

app_name = HomeConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]

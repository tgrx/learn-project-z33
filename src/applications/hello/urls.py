from django.urls import path

from applications.hello.apps import HelloConfig
from applications.hello.views import view_index
from applications.hello.views import view_reset
from applications.hello.views import view_update

app_name = HelloConfig.label

urlpatterns = [
    path("", view_index, name="index"),
    path("update/", view_update, name="update"),
    path("reset/", view_reset, name="reset"),
]

from django.urls import path

from applications.hello.views import view_index
from applications.hello.views import view_reset
from applications.hello.views import view_update

urlpatterns = [
    path("", view_index),
    path("update/", view_update),
    path("reset/", view_reset),
]

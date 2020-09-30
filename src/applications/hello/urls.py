from django.urls import path

from applications.hello.views import index
from applications.hello.views import update

urlpatterns = [
    path("", index),
    path("update/", update),
    path("reset/", index),
]

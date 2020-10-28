from django.urls import path

from applications.blog.apps import BlogConfig
from applications.blog.views import IndexView

app_name = BlogConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]

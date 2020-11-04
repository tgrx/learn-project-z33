from django.urls import path

from applications.blog.apps import BlogConfig
from applications.blog.views import IndexView
from applications.blog.views import NewPostView

app_name = BlogConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new/", NewPostView.as_view(), name="new-post"),
]

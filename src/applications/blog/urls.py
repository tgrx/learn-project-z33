from django.urls import path

from applications.blog import views
from applications.blog.apps import BlogConfig

app_name = BlogConfig.label

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.PostView.as_view(), name="post"),
    path("<int:pk>/delete/", views.DeletePostView.as_view(), name="delete-post"),
    path("<int:pk>/update/", views.UpdatePostView.as_view(), name="update-post"),
    path("new/", views.NewPostView.as_view(), name="new-post"),
]

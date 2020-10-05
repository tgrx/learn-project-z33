from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("applications.home.urls")),
    path("admin/", admin.site.urls),
    path("hello/", include("applications.hello.urls")),
]

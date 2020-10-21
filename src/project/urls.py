from django.contrib import admin
from django.urls import include
from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("", include("applications.home.urls")),
    path("admin/", admin.site.urls),
    path("hello/", include("applications.hello.urls")),
    path("sentry-debug/", trigger_error),
]

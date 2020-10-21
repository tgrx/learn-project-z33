from django.apps import AppConfig


class HomeConfig(AppConfig):
    label = "home"
    name = f"applications.{label}"

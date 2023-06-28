# pages.apps.py

from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = "pages"

    def ready(self):
        self.get_model("AboutUs")
        self.get_model("PageCGU")
        self.get_model("PageSupport")

# blog.apps.py

from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


class BlogConfig(AppConfig):
    name = "blog"
    label = "blog"
    verbose_name = "blog"

    def ready(self):
        blog = self.get_model("Post")
        pre_save.connect(receiver, sender=blog)

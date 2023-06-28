# comment.apps.py

from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


class CommentConfig(AppConfig):
    name = "comment"
    label = "comment"
    verbose_name = "comment"

    def ready(self):
        comment = self.get_model("Comment")
        pre_save.connect(receiver, sender=comment)

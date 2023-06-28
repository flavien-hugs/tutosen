# accounts.apps.py

from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


class AccountsConfig(AppConfig):
    name = "accounts"
    label = "accounts"
    verbose_name = "Compte utilisateur"

    def ready(self):
        users = self.get_model("User")
        pre_save.connect(receiver, sender=users)

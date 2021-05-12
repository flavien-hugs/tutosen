# accounts.apps.py

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'Compte utilisateur'

    def ready(self):
        import utils.signals # noqa
        self.get_model('User')

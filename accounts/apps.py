from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'compte utilisateur'

    def ready(self):
        import accounts.signals.handlers # noqa

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'compte utilisateur'

    def ready(self):
        try:
            import accounts.signals
        except ImportError:
            pass

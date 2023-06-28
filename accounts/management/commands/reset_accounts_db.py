from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    help = "Reset the database"

    def handle(self, *args, **options):
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Réinitialisation des utilisateurs"))

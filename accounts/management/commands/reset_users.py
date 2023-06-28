from django.core.management.base import BaseCommand

from ...models import Teacher, Student, User


class Command(BaseCommand):
    help = "Ajoute quelques utilisateurs de base"

    def handle(self, *args, **options):
        User.objects.all().delete()

        Teacher.objects.create(
            username="flavien-hugs", email="flavienhgs@pm.me", type=User.Types.TEACHER
        )
        Student.objects.create(
            username="fatima", email="flavienhugs@gmail.com", type=User.Types.STUDENT
        )
        self.stdout.write(self.style.SUCCESS("Réinitialisation des utilisateurs"))

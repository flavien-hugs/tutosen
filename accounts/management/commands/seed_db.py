# accounts/management/commands/seed_py.py

from django.core.management.base import BaseCommand

from faker import Faker
from accounts.models import Teacher


class Command(BaseCommand):
    help = "Seeds the database with 10 users"

    def handle(self, *args, **options):
        fake = Faker()
        # remove existing data
        Teacher.objects.all().delete()
        # add 10 users
        users = [Teacher(last_name=fake.last_name()) for index in range(10)]
        Teacher.objects.bulk_create(users)
        print("users created.")

# accounts.managers.py

import random
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(
                "Les utilisateurs doivent disposer d'une adresse électronique."
            )

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_active=True, last_login=now, date_joined=now, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le super-utilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le super-utilisateur doit avoir is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type="TEACHER")

    def get_recent_joined(self, **kwargs):
        queryset = self.get_queryset(**kwargs).filter(
            date_joined__lte=timezone.now(), **kwargs
        )
        return queryset

    def get_related(self, instance):
        teachers = self.get_queryset().filter(type=instance.type)
        return (teachers).exclude(id=instance.id).distinct()

    def recomended_teacher(self, instance):
        teacher = self.get_queryset().filter(user=instance.user).exclude(id=instance.id)
        teacher_list = random.shuffle(list(teacher))[:50]
        return teacher_list


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type="STUDENT")


class ParentOrTutorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type="PARENT_OR_TUTOR")

# accounts.managers.py

from django.db import models
from django.contrib.auth.models import BaseUserManager


class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        is_teacher = User.Types.TEACHER
        return super().get_queryset(*args, **kwargs).filter(type=is_teacher)


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        is_student = User.Types.STUDENT
        return super().get_queryset(*args, **kwargs).filter(type=is_student)
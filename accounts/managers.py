# accounts.managers.py

import random
from django.db import models
from django.utils import timezone


class TeacherManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='TEACHER')

    def get_recent_joined(self, **kwargs):
        queryset = self.get_queryset(**kwargs).filter(date_joined__lte=timezone.now(), **kwargs)
        print(queryset)
        return queryset

    def get_related(self, instance):
        teachers = self.get_queryset().filter(type=instance.type)
        return (teachers).exclude(id=instance.id).distinct()

    def recomended_teacher(self, instance):
        teacher = self.get_queryset().filter(
            user=instance.user).exclude(id=instance.id)
        teacher_list = random.shuffle(list(teacher))[:50]
        return teacher_list

    def create(self, **kwargs):
        kwargs.update({'type': 'TEACHER'})
        return super(TeacherManager, self).create(**kwargs)


class StudentManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='STUDENT')

    def create(self, **kwargs):
        kwargs.update({'type': 'STUDENT'})
        return super(StudentManager, self).create(**kwargs)


class ParentOrTutorManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='PARENT_OR_TUTOR')

    def create(self, **kwargs):
        kwargs.update({'type': 'PARENT_OR_TUTOR'})
        return super(ParentOrTutorManager, self).create(**kwargs)

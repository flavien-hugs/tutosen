import random
from django.db import models


class SubjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def get_courses_published(self):
        return super().get_queryset().filter(published=True)

    def get_category_related(self, instance):
        related_subject_category = (
            self.get_courses_published()
            .filter(category=instance.category)
            .exclude(id=instance.id)
            .distinct()
        )
        return related_subject_category

    def get_level_similar(self, instance):
        return self.get_courses_published().filter(level=instance.level)

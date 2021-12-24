# blog.managers.py

from django.db import models
from django.db.models import Q
from django.utils import timezone


class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            published=True,
            created_at__lte=now
        )

    def search(self, query):
        lookup = (
            Q(title__icontains=query)
            | Q(subtitle__icontains=query)
            | Q(body__icontains=query)
            | Q(meta_description__icontains=query)
            | Q(slug__icontains=query)
            | Q(author__first_name__icontains=query)
            | Q(author__last_name__icontains=query)
        )
        return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)

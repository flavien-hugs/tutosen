# courses.reviews.py

import uuid

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth import get_user_model

from courses.models import Subject
from django.template.defaultfilters import slugify


class Comment(models.Model):
    
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Subject ID'
    )
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='author'
    )
    course = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
        related_name='course',
        verbose_name='course'
    )
    rate = models.PositiveIntegerField(
        verbose_name="note",
        default=1
    )
    comment = models.TextField(
        max_length=500,
        verbose_name='comment',
        help_text='ajouter un commentaire'
    )
    date_added = models.DateTimeField(
        verbose_name='created at',
        auto_now=False,
        auto_now_add=True
    )
    parent = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        verbose_name="replies",
        related_name='replies',
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = 'comments'
        indexes = [
            models.Index(fields=['id', 'uuid']),
        ]

    def __str__(self):
        return f"Comment by {self.author.first_name} on {self.course.title}"


    def get_comment_detail_url(self):
        return reverse(
            "feedback:detail_feedback_url",
            kwargs={
                "link": self.author.link,
                "slug": self.course.slug
            }
        )

# pages.models.py

from django.db import models
from django.utils.text import Truncator
from django.utils.html import mark_safe

from ckeditor_uploader.fields import RichTextUploadingField


class AboutUs(models.Model):
    content = RichTextUploadingField(
        verbose_name='description',
        help_text="Description de l\'Entreprise: Activité, Mission, Objectif, etc"
    )

    class Meta:
        db_table = 'aboutus_db'
        verbose_name_plural = 'About Us'

    def __str__(self):
        truncated_content = Truncator(self.content)
        return mark_safe(truncated_content.words(10))


class PageCGU(models.Model):
    content = RichTextUploadingField(
        verbose_name='description de la CGU',
        help_text="Description de la Condition Générale d'Utilisation du site."
    )

    class Meta:
        db_table = 'cgu_db'
        verbose_name_plural = 'CGU'

    def __str__(self):
        truncated_content = Truncator(self.content)
        return mark_safe(truncated_content.chars(50))


class PageSupport(models.Model):
    content = RichTextUploadingField(
        verbose_name='description support',
        help_text="Description des questions"
    )

    class Meta:
        db_table = 'support_db'
        verbose_name_plural = 'Support'

    def __str__(self):
        truncated_content = Truncator(self.content)
        return mark_safe(truncated_content.chars(50))

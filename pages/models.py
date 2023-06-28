# pages.models.py

import datetime

from django.db import models
from django.utils.text import Truncator
from django.utils.html import mark_safe

from blog.models import Post


class AboutUs(models.Model):
    content = models.TextField(
        verbose_name="description",
        help_text="Description de l'Entreprise: Activité, Mission, Objectif, etc",
    )

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        truncated_content = Truncator(self.content)
        return mark_safe(truncated_content.words(10))


class PageCGU(models.Model):
    content = models.TextField(
        verbose_name="description de la CGU",
        help_text="Description de la Condition Générale d'Utilisation du site.",
    )

    class Meta:
        db_table = "cgu_db"
        verbose_name_plural = "CGU"

    def __str__(self):
        truncated_content = Truncator(self.content)
        return mark_safe(truncated_content.chars(50))


class PageSupport(models.Model):
    content = models.TextField(
        verbose_name="description support", help_text="Description des questions"
    )

    class Meta:
        db_table = "support_db"
        verbose_name_plural = "Support"

    def __str__(self):
        truncated_content = Truncator(self.content)
        return mark_safe(truncated_content.chars(50))


class Contact(models.Model):
    first_name = models.CharField(
        verbose_name="nom", max_length=80, help_text="votre nom"
    )
    last_name = models.CharField(
        verbose_name="prénom", max_length=80, help_text="votre prénom"
    )
    email = models.EmailField(
        verbose_name="email", max_length=180, help_text="votre adresse email"
    )
    phone = models.CharField(
        verbose_name="téléphone", max_length=24, help_text="votre numéro de téléphone"
    )
    reason = models.CharField(
        max_length=180, verbose_name="sujet", help_text="sujet du message"
    )
    message = models.TextField(verbose_name="message", help_text="votre message")
    date_added = models.DateField(
        verbose_name="date added", auto_now=False, auto_now_add=datetime.date.today
    )

    class Meta:
        ordering = ["-date_added"]
        verbose_name_plural = "Contact"

    def __str__(self):
        return f"{self.first_name} ({self.email})"

    def reason_display(self):
        return self.get_reason_display()


class Newsletters(models.Model):
    post = models.OneToOneField(to=Post, on_delete=models.PROTECT, verbose_name="post")
    email = models.CharField(verbose_name="email", unique=True, max_length=50)
    date_joinded = models.DateField(
        verbose_name="date joined", auto_now=False, auto_now_add=datetime.date.today
    )

    class Meta:
        ordering = ["-date_joinded"]
        verbose_name_plural = "Newsletters"
        indexes = [models.Index(fields=["id"], name="id_index_newsletter")]

    def __str__(self):
        return f"user {self.email} subscribe for {self.post.author} account"

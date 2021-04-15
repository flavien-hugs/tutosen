# pages.models.py

from django.db import models
from tinymce.models import HTMLField


class AboutUs(models.Model):
    
    content = HTMLField(
        verbose_name='description',
        help_text="Description de l\'Entreprise: Activité, Mission, Objectif, etc"
    )

    class Meta:
        db_table = 'aboutus_db'
        verbose_name_plural = 'qui sommes-nous'

    def __str__(self):
        return '{}'.format('Qui sommes-nous ?')

    def __repr__(self):
        return self.__str__()

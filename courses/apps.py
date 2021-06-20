# courses.apps.py

from django.apps import AppConfig
from django.dispatch import receiver
from django.db.models.signals import pre_save


class CoursesConfig(AppConfig):
    name = 'courses'
    label = 'courses'
    verbose_name = 'Courses'
    
    def ready(self):
        courses = self.get_model('Course')
        pre_save.connect(receiver, sender=courses)


    

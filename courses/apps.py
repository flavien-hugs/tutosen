# courses.apps.py

from django.apps import AppConfig
# from django.dispatch import receiver
# from django.db.models.signals import pre_save


class CoursesConfig(AppConfig):
    name = 'courses'

    def ready(self):
        import utils.signals # noqa

    #   courses = self.get_model('Courses')
    #   pre_save.connect(receiver, sender='app_label.Courses')

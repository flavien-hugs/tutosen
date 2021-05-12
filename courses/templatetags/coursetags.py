# courses.templatetags.coursetags.py

from django import template

from courses.models import Course

register = template.Library()


def model_name(self):
    try:
        return self.obj._meta.model_name
    except AttributeError:
        return None

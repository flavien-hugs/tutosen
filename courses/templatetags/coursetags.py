# courses.templatetags.coursetags.py

from django import template

register = template.Library()


def model_name(self):
    try:
        return self.obj._meta.model_name
    except AttributeError:
        return None

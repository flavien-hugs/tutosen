# courses.templatetags.coursetags.py

import time
import random

from django import template

from django.contrib.auth import get_user_model

register = template.Library()


@register.inclusion_tag("account/teacher/snippet/_snippet_teachers.html")
def instructors_list(count=25):
    instructors = get_user_model().objects.filter(type='TEACHER')[:count]
    random_instructor_show = sorted(instructors, key=lambda x:random.random())
    context = {'instructors': random_instructor_show}
    return context

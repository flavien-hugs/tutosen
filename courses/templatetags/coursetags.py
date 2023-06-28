import random

from django import template
from courses.models import Subject

register = template.Library()


@register.inclusion_tag("courses/snippets/_snippet_course_latest_list.html")
def latest_courses(count=25):
    courses = Subject.objects.get_courses_published().order_by("-created_at")[:count]
    random_courses = sorted(courses, key=lambda x: random.random())
    context = {"latest_course": random_courses}
    return context

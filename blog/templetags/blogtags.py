import random

from django import template
from blog.models import Blog

register = template.Library()


@register.inclusion_tag("blog/snippet/_snippet_blog_latest_list.html")
def latest_blog(count=25):
    courses = Blog.objects.get_courses_published().order_by("-created_at")[:count]
    random_courses = sorted(courses, key=lambda x: random.random())
    context = {"latest_course": random_courses}
    return context

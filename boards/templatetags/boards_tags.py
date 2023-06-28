# boards.templatetags.boards_tags.py

import hashlib
from django import template
from urllib.parse import urlencode
from django.utils.safestring import mark_safe

from courses.models import Subject

register = template.Library()


@register.filter
def gravatar_url(email, size=80):
    default = "mm"
    email = email.lower().encode("utf-8")
    url = "https://www.gravatar.com/avatar/{md5}?{params}".format(
        md5=hashlib.md5(email.lower()).hexdigest(),
        params=urlencode({"d": default, "s": str(size)}),
    )
    return url


@register.filter
def gravatar(email, size=80):
    url = gravatar_url(email, size)
    return mark_safe(
        f'<img src="{url}" width="{size}" height="{size}" class="avatar-xs \
        rounded-circle"/>'
    )


@register.simple_tag(takes_context=True)
def active_link(context, name):
    if context["request"].resolver_match.url_name == name:
        return "active rounded-0"
    return ""

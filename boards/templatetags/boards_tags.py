# boards.templatetags.boards_tags.py

import hashlib
from django import template
from urllib.parse import urlencode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def gravatar_url(email, size=80):
    default = 'mm'
    email = email.lower().encode('utf-8')
    url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
        md5=hashlib.md5(email.lower()).hexdigest(),
        params=urlencode({'d': default, 's': str(size)})
    )
    return url


@register.filter
def gravatar(email, size=80):
    url = gravatar_url(email, size)
    return mark_safe('<img src="{0}" width="{1}" height="{2}" class="avatar-xl rounded-circle"/>'.format(
        url, size, size)
    )


@register.simple_tag(takes_context=True)
def active_link(context, name):
    if context['request'].resolver_match.url_name == name:
        return 'active rounded-0'
    return ''

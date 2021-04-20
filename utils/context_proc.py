# utils.context_proc.py

from core import settings


def tutosen_context_processor(request):
    return {
        'title': settings.SITE_NAME,
        'addr_email': 'support@tutosen.com',
        'addr_contact': '01 51 57 13 96',
        'site_description': settings.SITE_DESCRIPTION,
        'site_keywords': settings.META_KEYWORDS,
        'request': request,
    }

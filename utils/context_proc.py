from core import settings


def tutosen_context_processor(request):
    return {
        "title": settings.SITE_NAME,
        "addr_email": "forum@bahut.com",
        "addr_contact": "(225) 077 772 848",
        "site_description": settings.SITE_DESCRIPTION,
        "site_keywords": settings.META_KEYWORDS,
        "request": request,
    }

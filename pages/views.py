# pages.views.py

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from pages.models import AboutUs, PageCGU, PageSupport


def aboutUsDetail(request, template='pages/ps-page.html'):
    about_content = get_object_or_404(AboutUs, pk=1)
    page_title = 'qui nous-sommes ?'
    page_heading = 'Vous voulez en savoir plus sur nous ?'
    context = {
        'page_title': page_title,
        'page_heading': page_heading,
        'content': about_content,
    }
    return render(request, template, context)


page_aboutus_view = aboutUsDetail


def pageCGUDetail(request, template='pages/ps-page.html'):
    cgu_content = get_object_or_404(PageCGU, pk=1)
    page_title = 'Foire aux questions'
    page_heading = 'Questions fréquemment posées'
    context = {
        'page_title': page_title,
        'page_heading': page_heading,
        'content': cgu_content,
    }
    return render(request, template, context)


page_cgu_detail = pageCGUDetail


def pageSupportetail(request, template='pages/ps-page.html'):
    support_content = get_object_or_404(PageSupport, pk=1)
    page_title = 'Condition Générale d\'Utilisation'
    page_heading = 'Politique de confidentialité et données personnelles'
    context = {
        'page_title': page_title,
        'page_heading': page_heading,
        'content': support_content,
    }
    return render(request, template, context)


page_support_detail = pageSupportetail

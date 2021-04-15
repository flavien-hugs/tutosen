# pages.views.py

from django.shortcuts import render
from django.shortcuts import get_object_or_404


def aboutUsDetail(request, template='pages/ps-page.html'):
    about_content = get_object_or_404(AboutUs, pk=1)
    page_title = 'qui nous-sommes ?'
    page_heading = 'Vous voulez en savoir plus sur nous ?'
    context = {
        'page_title': page_title,
        'page_heading': page_heading,
        'about_content': about_content,
    }
    return render(request, template, context)

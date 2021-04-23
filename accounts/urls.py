# accounts.urls.py

from django.urls import path
from django.views import generic


app_name = 'accounts'
urlpatterns = [
    path('trouver-un-instructeur/', generic.TemplateView.as_view(
        template_name='account/teacher/teacher_all.html',
        extra_context={'page_title': 'trouver votre instructeur'}),
        name='teacher_all_url'),

    path('instructeur/compte/detail/', generic.TemplateView.as_view(
        template_name='account/teacher/teacher_profile_detail.html',
        extra_context={'page_title': 'profile de l\'instructeur'}),
        name='teacher_profile_url'),
]

# pages.urls.py

from django.urls import path
from django.views import generic

from pages import views as pages_views


app_name = 'pages'
urlpatterns = [
    path(route='contact/', view=generic.TemplateView.as_view(
        template_name='pages/ps-contact.html',
        extra_context={'page_title': 'nous-contacter'}), name='contact'),
    path(route='qui-sommes-nous/', view=pages_views.page_aboutus_view, name='about_us'),
    path(route='conditition-generale-utilisation/', view=pages_views.page_cgu_detail, name='page_cgu'),
    path(route='support/', view=pages_views.page_support_detail, name='page_support'),
]

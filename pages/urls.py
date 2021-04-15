# pages.urls.py

from django.urls import path
from django.views import generic

from pages import views as pages_views


app_name = 'pages'
urlpatterns = [
    path('qui-sommes-nous/', pages_views.aboutUsDetail, name='about_us'),
    path('conditition-generale-utilisation/', pages_views.pageCGUDetail, name='page_cgu'),
    path('support/', pages_views.pageSupportetail, name='page_support'),
]

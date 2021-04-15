# pages.urls.py

from django.urls import path
from django.views import generic

from pages import views as pages_views


app_name = 'pages'
urlpatterns = [
    re_path('qui-sommes-nous/', pages_views.aboutUsDetail, name='about_us'),
]

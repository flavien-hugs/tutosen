# api.urls.py

from django.urls import path

from api import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path(route='users/', view=views.user_list_api_view),
    path(route='users/<int:pk>/', view=views.user_detail_api_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)

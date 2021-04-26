# accounts.urls.py

from django.urls import path
from django.views import generic

from accounts import views


app_name = 'accounts'
urlpatterns = [

    path(route="trouver-un-instructeur/",
        view=views.teacher_list_view, name='teacher_list_view'
    ),

    path(route='instructeur/<str:first_name>.<int:pk>/',
        view=views.teacher_detail_view, name='teacher_detail_view'),
]

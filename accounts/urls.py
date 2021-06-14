# accounts.urls.py

from django.urls import path

from accounts import views


app_name = 'accounts'
urlpatterns = [
    path(route="find/instructor/", view=views.teacher_list_view, name='teacher_list_view'),
    path(route='instructor/<uuid>/profile/', view=views.teacher_detail_view, name='teacher_detail_view'),
    path(route='check_validate_data', view=views.check_validate_data, name='check_validate_data')
]

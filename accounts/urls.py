# accounts.urls.py

from django.urls import path, include

from accounts.views import teachers


urlpatterns = [
    path('', include(([
        path(
            route="find/instructor/",
            view=teachers.teacher_list_view,
            name='teacher_list_view'
        ),

        path(
            route='instructor/<uuid>/profile/',
            view=teachers.teacher_profile_detail_view,
            name='teacher_detail_view'

        ),

        path(
            route='check_validate_data',
            view=teachers.check_validate_data,
            name='check_validate_data'
        )
    ], 'accounts'), namespace='accounts')),
]

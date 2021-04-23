# boards.urls.py

from django.views import generic
from django.urls import path, include

from accounts import views

app_name = 'boards'
urlpatterns = [

    path('redirect/', view=views.user_redirect_view, name="user_redirect"),
    path("update/<first_name>-<id>/", view=views.user_update_view, name="user_update"),
    path("delete/<first_name>-<id>/", view=views.user_delete_view, name="user_delete"),
    path("<first_name>-<id>/", view=views.user_detail_view, name="user_detail"),
    
    path('cours/add-course/', generic.TemplateView.as_view(
        template_name='dashboard/teacher/teacher_add_course.html',
        extra_context={'page_title': 'Ajouter un nouveau cours'}),
        name='teacher_add_course_url'),
]

# boards.urls.py

from django.urls import path

from django.views import generic


app_name = 'boards'
urlpatterns = [
    path('instructor/', generic.TemplateView.as_view(
        template_name='dashboard/teacher/teacher_dashboard.html',
        extra_context={'page_title': 'Tableau de bord Instructeur'}),
        name='teacher_dashboard_url'),

    path('cours/add/', generic.TemplateView.as_view(
        template_name='dashboard/teacher/teacher_add_course.html',
        extra_context={'page_title': 'Ajouter un nouveau cours'}),
        name='teacher_add_course_url'),
]

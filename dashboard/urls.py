# dashboard.urls.py

from django.urls import path

from django.views import generic


app_name = 'dashboard'
urlpatterns = [
    path('', generic.TemplateView.as_view(
        template_name='dashboard/teacher/teacher_dashboard.html',
        extra_context={'page_title': 'Tableau de bord Instructeur'}), name='teacher_dashboard_url'),
]

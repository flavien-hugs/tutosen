# courses.urls.py

from django.urls import path

from django.views import generic


app_name = 'courses'
urlpatterns = [
    path('tous-les-cours/', generic.TemplateView.as_view(
        template_name='courses/courses_list.html',
        extra_context={'page_title': 'tous les cours'}), name='courses_list_url'),

    path('detail/', generic.TemplateView.as_view(
        template_name='courses/courses_detail.html',
        extra_context={'page_title': 'detail du cours'}), name='courses_detail_url'),

    path('resume/', generic.TemplateView.as_view(
        template_name='courses/courses_resume.html',
        extra_context={'page_title': 'résume du cours'}), name='courses_resume_url'),
]

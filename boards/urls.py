# boards.urls.py

from django.urls import path
from django.views import generic

from accounts import views
from courses import views as courses_views

app_name = 'boards'
urlpatterns = [
    
    # /me/
    path(route='redirect/', view=views.user_redirect_view, name="user_redirect"),
    path(route="<pk>/", view=views.user_detail_view, name="user_detail"),
    path(route="parametres/<pk>/", view=views.user_update_view, name="user_update"),
    path(route="<pk>/delete_account/", view=views.user_delete_view, name="user_delete"),

    path(route="privacy-policy/", view=generic.TemplateView.as_view(
        template_name='dashboard/teacher/partials/_partial_profile_privacy.html',
        extra_context={'page_title': 'confidentialité du profil'}),
        name='teacher_profil_privacy_url'),

    # /me/course/
    path(route="course/all/", view=courses_views.course_list_view, name='teacher_list_cours_url'),
    path(route='course/create/', view=courses_views.course_create_view, name='teacher_add_course_url'),

    # /me/notifications/
    path(route="notifications/", view=generic.TemplateView.as_view(
        template_name='dashboard/teacher/partials/_partial_notification.html',
        extra_context={'page_title': 'Notification'}), name='teacher_notification_url'),
]

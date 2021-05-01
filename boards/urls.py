# boards.urls.py

from django.views import generic
from django.urls import path, include

from accounts import views

app_name = 'boards'
urlpatterns = [

    path(route='redirect/',
        view=views.user_redirect_view,
        name="user_redirect"),
    path(route="<str:first_name>.<int:pk>/settings/",
        view=views.user_update_view,
        name="user_update"),
    path(route="<str:first_name>.<int:pk>/delete/",
        view=views.user_delete_view,
        name="user_delete"),
    path(route="<str:first_name>.<int:pk>/",
        view=views.user_detail_view,
        name="user_detail"
    ),
    path(route="<str:first_name>.<int:pk>/update/description/",
        view=views.user_update_bio_view, 
        name="update_bio"
    ),
    path(route="<str:first_name>.<int:pk>/update/social-account/",
        view=views.user_social_profile_update_view,
        name='social_account_update'
    ),
    path(route="privacy-policy/", view=generic.TemplateView.as_view(
        template_name='dashboard/teacher/partials/_partial_profile_privacy.html',
        extra_context={'page_title': 'confidentialité du profil'}
        ), name='teacher_profil_privacy_url'
    ),

    path(route="notification/", view=generic.TemplateView.as_view(
        template_name='dashboard/teacher/partials/_partial_notification.html',
        extra_context={'page_title': 'Notification'}
        ), name='teacher_notification_url'
    ),

    path(route="cours/list/", view=generic.TemplateView.as_view(
        template_name='dashboard/teacher/teacher_list_cours.html',
        extra_context={'page_title': 'Liste de vos cours'}
        ), name='teacher_list_cours_url'
    ),

    path(route='cours/add-course/', view=generic.TemplateView.as_view(
        template_name='dashboard/teacher/teacher_add_course.html',
        extra_context={'page_title': 'Ajouter un nouveau cours'}
        ), name='teacher_add_course_url'),
]

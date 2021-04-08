# accounts.urls.py

from django.urls import path

from django.views import generic


app_name = 'accounts'
urlpatterns = [
    path('connexion/', generic.TemplateView.as_view(
        template_name='accounts/login.html',
        extra_context={'page_title': 'connexion'}), name='login_url'),

    path('inscription/', generic.TemplateView.as_view(
        template_name='accounts/signup.html',
        extra_context={'page_title': 'inscription'}), name='signup_url'),

    path('password/reset/', generic.TemplateView.as_view(
        template_name='accounts/password_reset.html',
        extra_context={'page_title': 'réinitialisation du mot de passe'}),
        name='password_reset_url'),

    path('teacher/all/', generic.TemplateView.as_view(
        template_name='accounts/teacher/teacher_all.html',
        extra_context={'page_title': 'trouver votre instructeur'}),
        name='teacher_all_url'),

    path('teacher/profile/detail/', generic.TemplateView.as_view(
        template_name='accounts/teacher/teacher_profile_detail.html',
        extra_context={'page_title': 'profile de l\'instructeur'}),
        name='teacher_profile_url'),
]

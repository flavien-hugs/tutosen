# accounts.adapter.py

from django.conf import settings
from django.http import HttpRequest
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.username = data['email']
        user.email = data['email']

        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()

        user.save()
        return user

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(
            settings, "ACCOUNT_ALLOW_REGISTRATION", True
        )

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            path = "/dashboard/{uuid}/"
            return path.format(uuid=request.user.uuid)

    def get_signup_redirect_url(self, request):
        if request.user.is_authenticated:
            path = "/dashboard/{uuid}/"
            return path.format(uuid=request.user.uuid)

    def get_logout_redirect_url(self, request):
        path = "/"
        return path

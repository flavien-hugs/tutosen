# accounts.adapter.py

from django.conf import settings
from django.http import HttpRequest
from django.forms import ValidationError
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(
            settings, "ACCOUNT_ALLOW_REGISTRATION", True
        )

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            path = "/dashboard/{first_name}-{id}/"
            return path.format(
                first_name=request.user.first_name,
                id=request.user.id,
            )

    def get_logout_redirect_url(self, request):
        path = "/"
        return path
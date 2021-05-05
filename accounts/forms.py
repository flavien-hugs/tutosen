# accounts.forms.py

from django import forms as d_forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, forms

from accounts.models import Teacher
from allauth.account.forms import SignupForm

CustomUser = get_user_model()


class UserChangeForm(forms.UserChangeForm):

    class Meta(forms.UserChangeForm.Meta):
        model = CustomUser


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {
            "duplicate_email": "Cette addresse est déjà utilisé par un autre utilisateur."
        }
    )

    class Meta(forms.UserCreationForm.Meta):
        model = CustomUser

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])


# CustomSignupForm hérite du module django-allauth SignupForm
class CustomSignupForm(SignupForm):

    civility = d_forms.TypedChoiceField(
        label="Civilité", choices=CustomUser.CIVILITY_CHOICES,
        initial='1', coerce=str, required=True,
    )
    first_name = d_forms.CharField(label="Votre nom de famille", max_length=100)
    last_name = d_forms.CharField(label="Votre prénom", max_length=100)

    type = d_forms.ChoiceField(
        label='Je suis un(e)',
        choices=[("STUDENT", "Étudiant(e)"), ("TEACHER", "Instructeur(trice)")],
        required=True,
    )
    privacy = d_forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # del self.fields["username"].widget.attrs["autofocus"]

    def custom_signup(self, request, user):

        user.type = self.cleaned_data["type"]
        user.privacy = self.cleaned_data['privacy']
        user.civility = self.cleaned_data['civility']
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']

        user.save()


class UserUpdateForm(d_forms.ModelForm):
    type = d_forms.ChoiceField(
        label='Je suis un',
        choices=[("TEACHER", "Instructeur"), ("STUDENT", "Étudiant(e)")],
        required=True,
    )

    class Meta:
        model = Teacher
        fields = [
            # user infos
            'type',
            'avatar',
            'civility',
            'username',
            'first_name',
            'last_name',

            # user adresse
            'country',
            'state',
            'phone_number',

            # prodil social accout
            'facebook',
            'twitter',
            'linkedin',

            # user description
            'brief_desc',
        ]

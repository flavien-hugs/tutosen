from django import forms
from django.contrib.auth import get_user_model

from accounts.models import Teacher

from allauth.account.forms import SignupForm

from django_summernote.widgets import SummernoteWidget

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhonePrefixSelect


class CustomSignupForm(SignupForm):

    civility = forms.TypedChoiceField(
        label="Civilité",
        choices=get_user_model().CIVILITY_CHOICES,
        initial="1",
        coerce=str,
        required=True,
    )
    first_name = forms.CharField(label="Votre nom de famille", max_length=100)
    last_name = forms.CharField(label="Votre prénom", max_length=100)

    type = forms.ChoiceField(
        label="Je suis un(e)",
        choices=[
            ("STUDENT", "Élève"),
            ("PARENT_OR_TUTOR", "Parent ou tuteur"),
            ("TEACHER", "Enseignant(e) ou professionnel(le)"),
        ],
        required=True,
    )

    privacy = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # del self.fields["username"].widget.attrs["autofocus"]

    def custom_signup(self, request, user):

        user.type = self.cleaned_data["type"]
        user.privacy = self.cleaned_data["privacy"]
        user.civility = self.cleaned_data["civility"]
        user.last_name = self.cleaned_data["last_name"]
        user.first_name = self.cleaned_data["first_name"]

        user.save()


class UserUpdateForm(forms.ModelForm):
    required_css_class = "required"

    country = CountryField(blank_label="Select country").formfield(
        widget=CountrySelectWidget(
            attrs={"class": "custom-select d-block w-100", "required": False}
        )
    )
    phone_number_prefix = PhoneNumberField(widget=PhonePrefixSelect(), region="CI")
    phone_number = PhoneNumberField(label="Téléphone", required=True)

    class Meta:
        model = Teacher
        fields = [
            # user infos
            "avatar",
            "statut",
            "civility",
            "first_name",
            "last_name",
            # user adresse
            "state",
            "country",
            "phone_number",
            # prodil social accout
            "twitter",
            "facebook",
            "linkedin",
            # user description
            "cover",
            "brief_desc",
        ]

        widgets = {"brief_desc": SummernoteWidget()}

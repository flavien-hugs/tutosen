# accounts.forms.py

from django import forms as d_forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, forms


from accounts import models
from allauth.account.forms import SignupForm

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):

    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {
            "duplicate_email": "Cette addresse est déjà utilisé par un autre utilisateur."
        }
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])


# CustomSignupForm hérite du module django-allauth SignupForm
class CustomSignupForm(SignupForm):

    # Spécifiez un champ de choix qui correspond
    # au champ de choix de notre modèle utilisateur.
    civility = d_forms.TypedChoiceField(
        label="Civilité", choices=User.CIVILITY_CHOICES,
        initial='1', coerce=str, required=True,
    )
    first_name = d_forms.CharField(label="Nom", max_length=100)
    last_name = d_forms.CharField(label="Prénom", max_length=100)
    type = d_forms.ChoiceField(
        label='Je suis un',
        choices=[("TEACHER", "Instructeur"), ("STUDENT", "Étudiant(e)")],
        required=True,
    )
    privacy = d_forms.BooleanField(required=True)

    # Remplacer la méthode init
    def __init__(self, *args, **kwargs):
        # Appeler l'init de la classe parente
        super().__init__(*args, **kwargs)
        
        # Supprimer l'autofocus parce qu'il est au mauvais endroit
        # del self.fields["username"].widget.attrs["autofocus"]

    # Mettre en place une logique d'inscription personnalisée
    def custom_signup(self, request, user):

        # Définir le type de l'utilisateur à partir de la
        # réponse au formulaire

        user.civility = self.cleaned_data['civility']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.type = self.cleaned_data["type"]
        user.privacy = self.cleaned_data['privacy']

        # Sauvegarder le type de l'utilisateur dans
        # sa fiche de base de données
        user.save()


class UpdateDescriptionForm(d_forms.ModelForm):
    class Meta:
        model = models.TeacherMore
        fields = ("brief_desc", 'qualification',)

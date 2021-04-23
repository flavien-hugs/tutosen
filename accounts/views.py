# accounts.views.teacher_views.py

from django.urls import reverse
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    slug_field = "first_name"
    slug_url_kwarg = "first_name"

user_detail_view = UserDetailView.as_view(
    template_name='dashboard/teacher/teacher_dashboard.html',
    extra_context={'page_title': 'Tableau de bord Instructeur'}
)


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'type', 'civility',]

    # Renvoyer l'utilisateur sur sa propre page
    # après une mise à jour réussie
    def get_success_url(self):
        return reverse(
            "accounts:account_detail",
            kwargs={
                'first_name': self.request.user.first_name.lower(),
                'id': self.request.user.id,
            },
        )

    def get_object(self):
        # Obtenir uniquement l'enregistrement de
        # l'utilisateur qui fait la demande
        return User.objects.get(
            first_name=self.request.user.first_name
        )

user_update_view = UserUpdateView.as_view(
    template_name='dashboard/teacher/partials/_partial_update_form.html',
    extra_context={'page_title': 'Mettre à jour votre profile'}
)


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    fields = [
        "first_name",
    ]

    model = User
    success_url = "home"

    def get_object(self):
        # Obtenir uniquement l'enregistrement de
        # l'utilisateur qui fait la demande
        return User.objects.get(
            first_name=self.request.user.first_name
        )

user_delete_view = UserDeleteView.as_view(
    template_name='dashboard/teacher/partials/_partial_delete_form.html',
    extra_context={'page_title': 'Suppression de compte'}
)


class UserRedirectView(LoginRequiredMixin, generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse(
            "accounts:account_detail",
            kwargs={
                'first_name': self.request.user.first_name.lower(),
                'id': self.request.user.id,
            },
        )

user_redirect_view = UserRedirectView.as_view()

# accounts.views.teacher_views.py

from django.views import generic
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from accounts.models import Teacher, TeacherMore
from accounts.forms import UserChangeForm, UpdateDescriptionForm, SocialProfileForm

# from accounts.decorators import teacher_required, student_required

CustomUser = get_user_model()


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    slug_field = "first_name"
    slug_url_kwarg = "first_name"
    login_url = 'account_login'

user_detail_view = UserDetailView.as_view(
    template_name='dashboard/teacher/teacher_dashboard.html',
    extra_context={'page_title': 'Tableau de bord Instructeur'}
)


class TeacherSocialProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    login_url = 'account_login'
    form_class = SocialProfileForm

    """Renvoyer l'utilisateur sur sa propre page
    après une mise à jour réussie"""

    def get_success_url(self):
        return reverse(
            "boards:user_detail",
            kwargs={
                'first_name': self.request.user.first_name.lower(),
                'pk': self.request.user.id,
            },
        )

    def get_object(self):
        current_user = self.request.user
        return current_user

    def form_valid(self, form):
        message = """Votre compte a été mise à jour avec succes !"""
        messages.success(self.request, message)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

user_social_profile_update_view = TeacherSocialProfileUpdateView.as_view(
    template_name='dashboard/teacher/partials/_partial_social_profile_form.html',
    extra_context={'page_title': 'Ajouter vos comptes réseaux sociaux'}
)


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    login_url = 'account_login'
    fields = ['civility', 'first_name', 'last_name', 'username', 'type',]

    """Renvoyer l'utilisateur sur sa propre page
    après une mise à jour réussie"""

    def get_success_url(self):
        return reverse(
            "boards:user_detail",
            kwargs={
                'first_name': self.request.user.first_name.lower(),
                'pk': self.request.user.id,
            },
        )

    def get_object(self):

        """ Obtenir uniquement l'enregistrement de
        l'utilisateur qui fait la demande """

        current_user = CustomUser.objects.get(
            first_name=self.request.user.first_name,
            last_name=self.request.user.last_name,
            id=self.request.user.id
        )

        return current_user

    def form_valid(self, form):
        message = """Votre compte a été mise à jour avec succes !"""
        messages.success(self.request, message)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

user_update_view = UserUpdateView.as_view(
    template_name='dashboard/teacher/partials/_partial_update_form.html',
    extra_context={'page_title': 'Mettre à jour votre profile'}
)


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = CustomUser
    login_url = 'account_login'
    success_url = reverse_lazy("home")

    def get_object(self):

        """ Obtenir uniquement l'enregistrement de
        l'utilisateur qui fait la demande"""

        current_user = CustomUser.objects.get(
            first_name=self.request.user.first_name,
            last_name=self.request.user.last_name,
            id=self.request.user.id
        )

        return current_user

    def delete(self, request, *args, **kwargs):
        msg = "Votre compte a été supprimer avec succès !"
        messages.success(request, msg)
        return super().delete(request, *args, **kwargs)

user_delete_view = UserDeleteView.as_view(
    template_name='dashboard/teacher/partials/_partial_delete_form.html',
    extra_context={'page_title': 'Suppression de compte'}
)


class UserRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse(
            "boards:user_detail",
            kwargs={
                'first_name': self.request.user.first_name.lower(),
                'pk': self.request.user.id,
            },
        )

user_redirect_view = UserRedirectView.as_view()


def update_bio(request):
    bio_form = UpdateDescriptionForm(request.POST or None, instance=request.user)
    try:
        if bio_form.is_valid():
            bio = bio_form.save(commit=False)
            bio.save()
            return JsonResponse(
                {
                    "code": "201",
                    "message": "Information bio mis a jour",
                    "is_success": True,
                }
            )
    except Exception as e:
        print(e)
        return JsonResponse(
            {"code": "500", "message": "Une erreur s'est produite", "is_success": False}
        )

user_update_bio_view = update_bio


class TeacherListView(generic.ListView):
    model = Teacher
    paginate_by = 100
    context_object_name = 'teacher_list'

    def get_queryset(self, *args, **kwargs):
        queryset = super(TeacherListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.order_by("-date_joined")
        return queryset


teacher_list_view = TeacherListView.as_view(
    template_name='account/teacher/teacher_list.html',
    extra_context={'page_title': 'trouver votre instructeur'}
)


class TeacherDetailView(generic.DetailView):
    model = Teacher


teacher_detail_view = TeacherDetailView.as_view(
    template_name='account/teacher/teacher_detail.html'
)


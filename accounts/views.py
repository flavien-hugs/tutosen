# accounts.views.teacher_views.py

from django.views import generic
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.models import Teacher
from accounts.decorators import teacher_required, student_required

User = get_user_model()


@method_decorator([login_required, teacher_required], name='dispatch')
class UserDetailView(generic.DetailView):
    model = User
    slug_field = "first_name"
    slug_url_kwarg = "first_name"

user_detail_view = UserDetailView.as_view(
    template_name='dashboard/teacher/teacher_dashboard.html',
    extra_context={'page_title': 'Tableau de bord Instructeur'}
)


@method_decorator([login_required, teacher_required], name='dispatch')
class UserUpdateView(generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'type', 'civility',]

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

        """Obtenir uniquement l'enregistrement de
        l'utilisateur qui fait la demande """

        return User.objects.get(
            first_name=self.request.user.first_name,
            last_name=self.request.user.last_name,
            id=self.request.user.id
        )

user_update_view = UserUpdateView.as_view(
    template_name='dashboard/teacher/partials/_partial_update_form.html',
    extra_context={'page_title': 'Mettre à jour votre profile'}
)


@method_decorator([login_required, teacher_required], name='dispatch')
class UserDeleteView(generic.DeleteView):

    model = User
    success_url = reverse_lazy("home")

    def get_object(self):

        """Obtenir uniquement l'enregistrement de
        l'utilisateur qui fait la demande"""

        return User.objects.get(
            first_name=self.request.user.first_name,
            last_name=self.request.user.last_name,
            id=self.request.user.id
        )

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


from django.http import JsonResponse
from accounts.forms import UpdateDescriptionForm

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
    paginaate_by = 100
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


# accounts.views.teacher_views.py

from django.views import generic
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts import mixins
from accounts.models import Teacher
from accounts.forms import UserUpdateForm

# from accounts.decorators import teacher_required, student_required

CustomUser = get_user_model()


class UserDetailView(LoginRequiredMixin, mixins.GetUserObject, generic.DetailView):
    login_url = 'account_login'
    queryset = CustomUser.objects.all()


user_detail_view = UserDetailView.as_view(
    template_name='dashboard/teacher/teacher_dashboard.html',
    extra_context={'page_title': 'Tableau de bord Instructeur'}
)


class UserUpdateView(LoginRequiredMixin, mixins.GetUserObject, generic.UpdateView):
    login_url = 'account_login'
    form_class = UserUpdateForm
    queryset = CustomUser.objects.all()
    success_message = "Votre profile a été mise à jour avec succes !"

    def get_success_url(self):
        return reverse(
            "boards:user_update",
            kwargs={'pk': self.object.uuid}
        )


user_update_view = UserUpdateView.as_view(
    template_name='dashboard/teacher/partials/_partial_update_form.html',
    extra_context={'page_title': 'Mettre à jour votre profile'}
)


class UserDeleteView(LoginRequiredMixin, mixins.GetUserObject, generic.DeleteView):
    login_url = 'account_login'
    success_url = reverse_lazy("home")
    queryset = CustomUser.objects.all()
    success_message = "Votre profile a été supprimer avec succès !"

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


user_delete_view = UserDeleteView.as_view(
    template_name='dashboard/teacher/partials/_partial_delete_form.html',
    extra_context={'page_title': 'Suppression de compte'}
)


class UserRedirectView(generic.RedirectView):

    permanent = True
    query_string = True
    pattern_name = 'user_detail'

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            "boards:user_detail",
            kwargs={'pk': self.object.uuid}
        )


user_redirect_view = UserRedirectView.as_view()


class TeacherListView(generic.ListView):
    paginate_by = 100
    context_object_name = 'teacher_list'
    queryset = Teacher.objects.order_by('-date_joined')

    def head(self, *args, **kwargs):
        last_teacher_register = self.get_queryset().latest('date_joined')
        response = HttpResponse()
        response['Last-Modified'] = last_teacher_register.date_joined.strftime(
            '%a, %d %b %Y %H:%M:%S GMT')
        return response


teacher_list_view = TeacherListView.as_view(
    template_name='account/teacher/teacher_list.html',
    extra_context={'page_title': 'trouver votre instructeur'}
)


class TeacherDetailView(generic.DetailView):
    model = Teacher


teacher_detail_view = TeacherDetailView.as_view(
    template_name='account/teacher/teacher_detail.html'
)

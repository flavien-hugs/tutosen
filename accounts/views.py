# accounts.views.teacher_views.py

import time

from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts import mixins as amxs
from accounts.models import Teacher
from accounts.forms import UserUpdateForm

# from accounts.decorators import teacher_required, student_required

CustomUser = get_user_model()


def check_validate_data_view(request):
    """
    Check form availability
    """
    check_email = request.GET.get('email', None)
    response = {
        'email_is_taken': CustomUser.objects.filter(email__iexact=check_email).exists()
    }

    return JsonResponse(response)


check_validate_data = check_validate_data_view


class UserDashboardDetailView(LoginRequiredMixin, amxs.GetUserObject, generic.DetailView):
    model = CustomUser
    login_url = reverse_lazy('account_login')


user_detail_view = UserDashboardDetailView.as_view(
    template_name='dashboard/teacher/teacher_dashboard.html',
    extra_context={'page_title': 'Tableau de bord'}
)


class UserProfileUpdateView(LoginRequiredMixin, amxs.GetUserObject, amxs.AjaxResponseMixin, generic.UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    login_url = reverse_lazy('account_login')
    success_message = "Votre profile a été mise à jour avec succes !"

    def get_success_url(self):
        return reverse(
            "boards:user_update", kwargs={'pk': self.object.uuid}
        )


user_update_view = UserProfileUpdateView.as_view(
    extra_context={'page_title': 'Mettre à jour votre profile'},
    template_name='dashboard/teacher/partials/_partial_update_form.html',
)


class UserProfileDeleteView(LoginRequiredMixin, amxs.GetUserObject, generic.DeleteView):
    login_url = reverse_lazy('account_login')
    success_url = reverse_lazy("home")
    queryset = CustomUser.objects.all()
    success_message = "Votre profile a été supprimer avec succès !"

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


user_delete_view = UserProfileDeleteView.as_view(
    template_name='dashboard/teacher/partials/_partial_delete_form.html',
    extra_context={'page_title': 'Suppression de compte'}
)


class UserRedirectView(generic.RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'user_detail'

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            "boards:user_detail", kwargs={'pk': self.object.uuid}
        )


user_redirect_view = UserRedirectView.as_view()


class UserProfileListView(amxs.InstructorSearchMixin, generic.ListView):
    paginate_by = 150
    context_object_name = 'teacher_list'
    queryset = Teacher.objects.order_by('-date_joined')

    def head(self, *args, **kwargs):
        last_teacher_register = self.get_queryset().latest('date_joined')
        response = HttpResponse()
        response['Last-Modified'] = last_teacher_register.date_joined.strftime(
            '%a, %d %b %Y %H:%M:%S GMT')
        return response


teacher_list_view = UserProfileListView.as_view(
    template_name='account/teacher/teacher_list.html',
    extra_context={'page_title': 'trouver votre instructeur'}
)


class UserProfileDetailView(generic.DetailView):
    model = Teacher
    slug_field = "uuid"
    slug_url_kwarg = 'uuid'
    context_object_name = 'teacher_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object.get_fullname()
        context['page_title'] = 'profile de "{0}"'.format(profile)
        return context


teacher_detail_view = UserProfileDetailView.as_view(
    template_name='account/teacher/teacher_detail.html'
)

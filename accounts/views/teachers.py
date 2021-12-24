# accounts.views.teacher_views.py

from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin

from blog.models import Post
from courses.models import Subject

from accounts import models, forms, mixins


def check_validate_data_view(request):
    check_email = request.GET.get('email', None)
    response = {
        'email_is_taken': get_user_model().objects.filter(
            email__iexact=check_email).exists()
    }

    return JsonResponse(response)


check_validate_data = check_validate_data_view


class TeacherDashboardDetailView(
    LoginRequiredMixin,
    mixins.GetUser,
    generic.DetailView
):
    """
    Provide a detail of Teacher object
    """

    slug_field = "link"
    slug_url_kwarg = "link"
    model = models.Teacher
    template_name = 'dashboard/teacher/teacher_dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['subjects'] = Subject.objects.get_courses_published().filter(
            instructor=self.request.user)[0:5]
        return super(TeacherDashboardDetailView, self).get_context_data(**kwargs)


teacher_detail_view = TeacherDashboardDetailView.as_view(
    extra_context={'page_title': 'tableau de bord'}
)


class TeacherProfileUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.TeacherUpdateMixin,
    generic.UpdateView
):  
    
    """
    Provide a update of Teacher object
    """
    
    slug_field = "link"
    slug_url_kwarg = "link"
    model = get_user_model()
    form_class = forms.UserUpdateForm
    success_message = "Account successfully update !"
    template_name = 'dashboard/teacher/partials/_partial_update_form.html'

teacher_update_view = TeacherProfileUpdateView.as_view(
    extra_context={'page_title': 'Mettre à jour votre profile'}
)


class TeacherProfileDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView
):  

    """
    Provide a delete of Teacher object
    """

    slug_field = "link"
    slug_url_kwarg = "link"
    model = get_user_model()
    success_url = reverse_lazy("home")
    success_message = "Account successfully deleted !"
    template_name = 'dashboard/teacher/partials/_partial_delete_form.html'

    def delete(self, request, *args, **kwargs):
        return super(TeacherProfileDeleteView, self).delete(request, *args, **kwargs)


teacher_delete_view = TeacherProfileDeleteView.as_view(
    extra_context={'page_title': 'Suppression de compte'}
)


class TeacherProfileListView(mixins.TeacherSearchMixin, generic.ListView):
    """
    Provide a list of Teacher object
    """
    paginate_by = 25
    context_object_name = 'teacher_list'
    queryset = models.Teacher.objects.order_by('-date_joined')
    template_name = 'account/teacher/teacher_list.html'


teacher_list_view = TeacherProfileListView.as_view(
    extra_context={'page_title': 'find instructor'}
)


class TeacherProfileDetailView(generic.DetailView):
    """
    Provide a detail of Teacher object
    """
    slug_field = "link"
    slug_url_kwarg = "link"
    model = models.Teacher
    context_object_name = 'teacher'
    template_name='account/teacher/teacher_detail.html'

    def get_context_data(self, **kwargs):
        fullname = self.object.get_fullname()
        kwargs['page_title'] = f'profile de "{fullname}"'
        return super(TeacherProfileDetailView, self).get_context_data(**kwargs)


teacher_profile_detail_view = TeacherProfileDetailView.as_view()


class TeacherCourseListView(MultipleObjectMixin, generic.DetailView):
    """
    Provide a course of Teacher object
    """
    paginate_by = 20
    slug_field = "link"
    slug_url_kwarg = "link"
    model = models.Teacher
    template_name='account/teacher/teacher_post_list.html'

    def get_context_data(self, **kwargs):
        teacher = self.get_object()
        page_title = f'post list for "{teacher.get_fullname()}"'
        object_list = Subject.objects.get_courses_published().filter(instructor=self.get_object())
        return super(TeacherCourseListView, self).get_context_data(
            teacher=teacher,
            page_title=page_title,
            object_list=object_list,
            **kwargs
        )


teacher_course_view = TeacherCourseListView.as_view()


class TeacherPostListView(MultipleObjectMixin, generic.DetailView):
    """
    Provide a blog of Teacher object
    """
    paginate_by = 20
    slug_field = "link"
    slug_url_kwarg = "link"
    model = models.Teacher
    template_name='account/teacher/teacher_post_list.html'

    def get_context_data(self, **kwargs):
        teacher = self.get_object()
        page_title = f'post list for "{teacher.get_fullname()}"'
        object_list = Post.objects.published().filter(author=self.get_object())
        return super(TeacherPostListView, self).get_context_data(
            teacher=teacher,
            page_title=page_title,
            object_list=object_list,
            **kwargs
        )


teacher_blog_view = TeacherPostListView.as_view()

# courses.views.py

from django.urls import reverse_lazy
from django.views import generic as mxs
from django.contrib.auth import mixins as auth_mxs

from courses import mixins


class CourseListView(mixins.InstructorCourseMixin, mxs.ListView):
    template_name = 'dashboard/courses/teacher_list_cours.html'


course_list_view = CourseListView.as_view(
    extra_context={'page_title': 'liste de vos cours'}
)


class CourseCreateView(auth_mxs.PermissionRequiredMixin, mixins.InstructorCourseEditMixin, mxs.CreateView):
    permission_required = 'courses.add_course'


course_create_view = CourseCreateView.as_view(
    extra_context={'page_title': 'ajouter un nouveau cours'}
)


class CourseUpdateView(auth_mxs.PermissionRequiredMixin, mixins.InstructorCourseEditMixin, mxs.UpdateView):
    permission_required = 'courses.update_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'edit course "{0}"'.format(self.object.course_title)
        return context


course_update_view = CourseUpdateView.as_view()


class CourseDeleteView(auth_mxs.PermissionRequiredMixin, mixins.InstructorCourseEditMixin, mxs.DeleteView):
    template_name = 'cours/gestion/cours/supprimer_cours.html'
    success_url = reverse_lazy('cours:gestion_liste_cours')
    permission_required = 'courses.delete_course'


course_delete_view = CourseDeleteView.as_view()

# courses.views.py

from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic as mxs
from django.contrib.auth import mixins as auth_mxs

from courses import mixins, models, forms

class CourseListView(mixins.InstructorCourseMixin, mxs.ListView):
    template_name = 'dashboard/courses/teacher_list_courses.html'


course_list_view = CourseListView.as_view(
    extra_context={'page_title': 'liste de vos cours'}
)


class CourseCreateView(auth_mxs.PermissionRequiredMixin, mixins.InstructorCourseEditMixin, mxs.CreateView):
    model = models.Course
    permission_required = 'courses.add_course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['titles'] = forms.course_chapter_formset(self.request.POST)
        else:
            context['titles'] = forms.course_chapter_formset()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:teacher_list_cours_url', kwargs={'uuid': str(self.object.uuid)})


course_create_view = CourseCreateView.as_view(
    extra_context={'page_title': 'ajouter un nouveau cours'}
)


class CourseUpdateView(auth_mxs.PermissionRequiredMixin, mixins.InstructorCourseEditMixin, mxs.UpdateView):
    permission_required = 'courses.update_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'edit course "{0}"'.format(self.object.course_title)
        if self.request.POST:
            context['titles'] = Coforms.course_chapter_formsetllectionTitleFormSet(
                self.request.POST, instance=self.object)
        else:
            context['titles'] = forms.course_chapter_formset(instance=self.object)
        return context


course_update_view = CourseUpdateView.as_view()


class CourseDeleteView(auth_mxs.PermissionRequiredMixin, mixins.InstructorCourseEditMixin, mxs.DeleteView):
    template_name = 'cours/gestion/cours/supprimer_cours.html'
    success_url = reverse_lazy('cours:gestion_liste_cours')
    permission_required = 'courses.delete_course'


course_delete_view = CourseDeleteView.as_view()

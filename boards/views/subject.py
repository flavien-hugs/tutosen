# courses.views.course.py

from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages import views

from courses import models
from accounts import mixins
from boards.forms import SubjectForm


class SubjectListView(mixins.TeacherSubjectMixin, generic.ListView):
    paginate_by = 20
    model = models.Subject
    context_object_name = "subject_list"
    template_name = 'dashboard/courses/manage/subject/subject_list.html'

    def get_queryset(self):
        subject = self.model.objects.filter(
            instructor=self.request.user
        )
        return subject


subject_list_view = SubjectListView.as_view(
    extra_context={
        'page_title': 'liste de vos cours',
        'empty_subject_label': "Adding course",
        'empty_subject_content': "Vous n'avez aucun cours actuellement.",
    }
)


class SubjectCreateView(
    views.SuccessMessageMixin,
    mixins.TeacherSubjectEditMixin,
    generic.CreateView
):  
    success_message = "Course successfully created !"


subject_create_view = SubjectCreateView.as_view(
    extra_context={
        'page_title': 'create new course'
    }
)


class SubjectUpdateView(
    views.SuccessMessageMixin,
    mixins.TeacherSubjectEditMixin,
    generic.UpdateView
):
    success_message = "Course successfully updated !"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubjectForm(
            instance=self.get_object()
        )
        context['page_title'] = f'Update Course "{self.object.title}"'
        return context


subject_update_view = SubjectUpdateView.as_view()


class SubjectDeleteView(
    views.SuccessMessageMixin,
    mixins.TeacherSubjectEditMixin,
    generic.DeleteView
):
    success_message = "Course successfully delete !"
    template_name = 'dashboard/courses/manage/subject/delete_subject.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Delete Course "{self.object.title}"'
        return context


subject_delete_view = SubjectDeleteView.as_view()

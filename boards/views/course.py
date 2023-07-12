# courses.views.course.py

from django.db import transaction
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages import views


from boards import forms
from courses import models
from accounts import mixins


class CourseListView(generic.DetailView):
    paginate_by = 10
    model = models.Subject
    context_object_name = "courses"
    template_name = 'dashboard/courses/manage/course/list_courses.html'

    def get_queryset(self):
        courses = self.model.objects.filter(instructor=self.request.user)
        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapiter'] = self.get_object()
        context['empty_subject_label'] = "Adding new chapiter"
        context['empty_subject_content'] =  "Vous n'avez aucun cours actuellement."
        context['page_title'] = f'Chapiters this course "{self.object.title}"'
        return context


course_list_view = CourseListView.as_view()


class CourseCreateView(
    views.SuccessMessageMixin,
    mixins.TeacherCourseCreateMixin,
    generic.CreateView
):
    success_message = "Chapiter successfully created !"

    def get_context_data(self, **kwargs):
        if self.request.POST:
            kwargs['form'] = self.form_class(
                self.request.POST, instance=self.get_object()
            )
        else:
            kwargs['form'] = self.form_class()
        kwargs['chapiter'] = self.get_object()
        kwargs['page_title'] = f'Create chapiter this course "{self.get_object()}"'
        return super(CourseCreateView, self).get_context_data(**kwargs)


course_create_view = CourseCreateView.as_view()


class CourseUpdateView(
    views.SuccessMessageMixin,
    mixins.TeacherCourseUpdateMixin,
    generic.UpdateView
):
    success_message = "Chapiter successfully updated !"

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        kwargs['title'] = obj
        kwargs['chapiter'] = obj.subject
        kwargs['page_title'] = f'Update chapiter "{obj.title}"'
        return super(CourseUpdateView, self).get_context_data(**kwargs)


course_update_view = CourseUpdateView.as_view()


class CourseDeleteView(views.SuccessMessageMixin, generic.DeleteView):
    model = models.Course
    permission_required = 'course.delete_course'
    success_message = "Chapiter successfully delete !"

    def get_success_url(self):
        return reverse_lazy(
            'course:list_course_url',
            kwargs={
                'username': self.get_object().subject.instructor.get_first_name(),
                'slug': self.get_object().subject.slug,
            }
        )


course_delete_view = CourseDeleteView.as_view()

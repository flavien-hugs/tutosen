# courses.mixins.py

from django.urls import reverse_lazy
from django.contrib.auth import mixins

from courses.models import Course


class InstructorMixin:

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_filter = queryset.filter(instructor=self.request.user)
        return queryset_filter


class InstructorMixinEdit:

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)


class InstructorCourseMixin(InstructorMixin, mixins.LoginRequiredMixin):
    model = Course
    fields = [
        'course_language', 'course_title', 'course_category',
        'course_brief', 'course_fee'
    ]
    success_url = reverse_lazy('courses:teacher_list_cours_url')


class InstructorCourseEditMixin(InstructorCourseMixin, InstructorMixinEdit):
    template_name = 'dashboard/courses/teacher_add_course.html'


class StudentMixin:

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_filter = queryset.filter(student=self.request.user)
        return queryset_filter


class ParentOrTutorMixin:

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_filter = queryset.filter(parent_or_tutor=self.request.user)
        return queryset_filter

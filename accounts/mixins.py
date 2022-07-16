# accounts.mixins.py

from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from courses.models import Subject, Course
from boards.forms import SubjectForm, CourseForm, CourseFormSet


class GetUser(UserPassesTestMixin, object):

    login_url = 'account_login'

    def get_object(self):

        current_user = get_user_model().objects.get(
            pk=self.request.user.pk
        )
        current_user.last_accessed = timezone.now()
        current_user.save()
        return current_user

    def test_func(self):
        obj = self.get_object()
        print(obj.type) # return TEACHER
        return obj.type == "TEACHER"


class TeacherMixin(LoginRequiredMixin, object):
    def get_queryset(self):
        queryset = super(TeacherMixin, self).get_queryset()
        return queryset.filter(instructor=self.request.user)


class TeacherEditMixin(object):
    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super(TeacherEditMixin, self).form_valid(form)


class TeacherSubjectMixin(TeacherMixin):
    model = Subject
    form_class = SubjectForm

    def form_valid(self, form, *args, **kwargs):
        course = form.save(commit=False)
        image = form.cleaned_data['image']
        course.instructor = self.request.user
        form.instance.instructor = self.request.user
        course.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_subject_list_url()


class TeacherSubjectEditMixin(TeacherSubjectMixin, TeacherEditMixin):
    template_name = 'dashboard/courses/manage/subject/form_subject.html'


class TeacherCourseMixin(object):
    template_name = 'dashboard/courses/manage/course/form_course.html'

    def get_success_url(self):
        return self.get_object().get_course_list_url()


class TeacherCourseCreateMixin(TeacherCourseMixin):
    model = Subject
    form_class = CourseFormSet

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        with transaction.atomic():
            form.instance.instructor = self.request.user
            self.object = form.save()
            
            if form.is_valid():
                form.instance = self.get_object()
                form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_object().get_subject_course_list_url()


class TeacherCourseUpdateMixin(TeacherCourseMixin):
    model = Course
    form_class = CourseForm

    def form_valid(self, form):
        subject = form.save(commit=False)
        form.instance.subject.instructor = self.request.user
        subject.save()
        return super().form_valid(form)


class TeacherUpdateMixin(object):

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = self.form_class(
                request.POST or None,
                request.FILES,
                instance=request.user
            )
            if form.is_valid():
                self.object = form.save()
                return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_userupdate_url()


class GetStudent(UserPassesTestMixin, object):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.pk)

    def test_func(self):
        obj = self.get_object()
        print(obj.type)
        return obj.type == "STUDENT"
    

class ParentOrTutorMixin(UserPassesTestMixin, object):
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_filter = queryset.filter(parent_or_tutor=self.request.user)
        return queryset_filter

    def test_func(self):
        obj = self.get_object()
        print(obj.type) # return PARENT_OR_TUTOR
        return obj.type == "PARENT_OR_TUTOR"


class TeacherSearchMixin(object):
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        q = self.request.GET.get('q', None)
        if q:
            lookups = (
                Q(statut__icontains=q)
                | Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(brief_desc__icontains=q)
                | Q(country__icontains=q)
                | Q(state__icontains=q)
            )
            return queryset.filter(lookups).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', None)
        if query:
            kwargs['page_title'] = f'Recherche pour "{query}"'
        return super().get_context_data(**kwargs)

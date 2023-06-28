from django.db import transaction
from django.views import generic as mxs
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.forms.models import modelform_factory
from django.contrib.auth import mixins as auth_mxs
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin

from courses import models, forms


class ChapterListView(auth_mxs.LoginRequiredMixin, mxs.DetailView):
    paginate_by = 10
    model = models.Course
    context_object_name = "chapiters"
    template_name = "dashboard/courses/manage/chapter/chapter_list.html"

    def get_queryset(self):
        course_chapiter = self.model.objects.filter(instructor=self.request.user)
        return course_chapiter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f'Course "{self.object.title}!r" chapiters'
        return context


chapter_list_view = ChapterListView.as_view()


class ChapterCreateView(
    auth_mxs.LoginRequiredMixin, SuccessMessageMixin, mxs.CreateView
):

    model = models.Course
    form_class = forms.ChapterFormSet
    success_message = "Course chapiter successfully created !"
    template_name = "dashboard/courses/manage/chapter/chapter_form.html"

    def get_context_data(self, **kwargs):
        context = super(ChapterCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["form"] = self.form_class(
                self.request.POST, self.request.FILES, instance=self.get_object()
            )
        else:
            context["form"] = self.form_class()
        context["chapiter"] = self.get_object()
        context["page_title"] = f'Add new chapiter this course "{self.get_object()}"!r'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = context["form"]
        with transaction.atomic():
            form.instance.instructor = self.request.user
            self.object = form.save()
        if form.is_valid():
            form.instance = self.get_object()
            form.save()
        return super(ChapterCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "course_chapter:chapter_list_url",
            kwargs={
                "username": self.get_object().instructor.get_first_name(),
                "slug": self.get_object().slug,
            },
        )


chapter_create_view = ChapterCreateView.as_view()


class ChapterUpdateView(
    auth_mxs.LoginRequiredMixin, SuccessMessageMixin, mxs.UpdateView
):
    model = models.CourseChapter
    form_class = forms.ChapterForm
    context_object_name = "chapiter"
    success_message = "Course chapiter successfully updated !"
    template_name = "dashboard/courses/manage/chapter/chapter_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "course_chapter:chapter_list_url",
            kwargs={
                "username": self.get_object().course.instructor.get_first_name(),
                "slug": self.get_object().course.slug,
            },
        )

    def form_valid(self, form):
        course = form.save(commit=False)
        form.doc = form.cleaned_data["doc"]
        form.instance.instructor = self.request.user
        course.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapiter"] = self.get_object()
        context["page_title"] = f"Update chapiter {self.get_object().title}!r"
        return context


chapter_update_view = ChapterUpdateView.as_view()


class ChapterDeleteView(
    auth_mxs.LoginRequiredMixin, SuccessMessageMixin, mxs.DeleteView
):
    model = models.CourseChapter
    success_message = "Course chapiter successfully delete !"

    def get_success_url(self):
        return reverse_lazy(
            "course_chapter:chapter_list_url",
            kwargs={
                "username": self.get_object().course.instructor.get_first_name(),
                "slug": self.get_object().course.slug,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapiter"] = self.get_object()
        context["page_title"] = f"Delete chapiter {self.get_object()}!r"
        return context


chapter_delete_view = ChapterDeleteView.as_view()
